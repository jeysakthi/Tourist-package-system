from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, PackageForm
from .models import Package, Booking
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Vendor
from .forms import VendorRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Package, Booking
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from .models import Vendor
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,HttpResponse
from .models import Package
from .forms import PackageForm


@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = "Approved"
    booking.save()
    return redirect('vendor_dashboard')

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = "Rejected"
    booking.save()
    return redirect('vendor_dashboard')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'Paid'
        booking.save()
        return render(request, 'tourapp/payment_success.html', {'booking': booking})


@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    amount = int(booking.package.price * booking.persons)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    booking.razorpay_order_id = razorpay_order['id']
    booking.save()

    context = {
        "booking": booking,
        "order_id": razorpay_order['id'],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
    }
    return render(request, "tourapp/payment.html", context)

@login_required
def create_booking(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        persons = int(request.POST.get('persons'))

        booking = Booking.objects.create(
            user=request.user,
            package=package,
            booking_date=booking_date,
            persons=persons,
            status='Pending'
        )
        return redirect('payment', booking_id=booking.id)

    return render(request, 'tourapp/booking_form.html', {'package': package})

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'tourapp/booking_detail.html', {'booking': booking})
@login_required
def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if package.vendor.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this package.")

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = PackageForm(instance=package)

    return render(request, 'tourapp/edit_package.html', {'form': form, 'package': package})


@login_required
def delete_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    # Only the vendor who owns the package can delete it
    if package.vendor.user != request.user:
        return HttpResponse("You are not allowed to edit this package.", status=403)


    if request.method == 'POST':
        package.delete()
        return redirect('vendor_dashboard')  # redirect after deletion confirmation

    return render(request, 'tourapp/delete_package_confirm.html', {'package': package})



def home(request):
    return render(request, 'tourapp/home.html')




def user_register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'tourapp/register.html', {
                'error': 'Passwords do not match',
                'register_type': 'user'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'tourapp/register.html', {
                'error': 'Username already exists',
                'register_type': 'user'
            })

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'tourapp/register.html', {'register_type': 'user'})

def login_user(request):
    login_type = request.GET.get('type', 'user') 

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            elif hasattr(user, 'vendor'):
                return redirect('vendor_dashboard')
            else:
                return redirect('dashboard')
        else:
            return render(request, 'tourapp/login.html', {
                'error': 'Invalid credentials',
                'login_type': login_type
            })

    return render(request, 'tourapp/login.html', {
        'login_type': login_type
    })


def logout_user(request):
    logout(request)
    return redirect('home')



def package_list(request):
    packages = Package.objects.filter(expiry_date__gte=timezone.now(), is_approved=True)

    destination = request.GET.get('destination')
    price_sort = request.GET.get('price')
    top = request.GET.get('top')
    budget = request.GET.get('budget')

    if destination:
        packages = packages.filter(location__icontains=destination)
    if price_sort == 'low':
        packages = packages.order_by('price')
    elif price_sort == 'high':
        packages = packages.order_by('-price')
    if top:
        packages = packages.filter(is_top_package=True)
    if budget:
        packages = packages.filter(is_budget_friendly=True)

    return render(request, 'tourapp/package_list.html', {'packages': packages})


def package_detail(request, id):
    package = Package.objects.get(id=id)
    return render(request, 'tourapp/package_detail.html', {'package': package})



@login_required
def dashboard(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'tourapp/dashboard.html', {'bookings': user_bookings})

@login_required
def add_package(request):
    form = PackageForm()
    if request.method == "POST":
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user.vendor
            package.save()
            return redirect('vendor_dashboard')
    return render(request, 'tourapp/add_package.html', {'form': form})



def vendor_register(request):
    form = VendorRegisterForm()
    if request.method == 'POST':
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Vendor.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name']
            )
            return redirect('login')
    return render(request, 'tourapp/register.html', {'form': form, 'vendor': True})



def vendor_register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'tourapp/register.html', {
                'error': 'Passwords do not match',
                'register_type': 'vendor'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'tourapp/register.html', {
                'error': 'Username already exists',
                'register_type': 'vendor'
            })

        user = User.objects.create_user(username=username, email=email, password=password)
        Vendor.objects.create(user=user)  
        login(request, user)
        return redirect('vendor_dashboard')

    return render(request, 'tourapp/register.html', {'register_type': 'vendor'})


@login_required
def book_package(request, id):
    package = Package.objects.get(id=id)
    Booking.objects.create(user=request.user, package=package)
    return render(request, 'tourapp/booking_confirm.html', {'package': package})



def initiate_payment(request, id):
    package = Package.objects.get(id=id)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": int(package.price * 10000),  
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, 'tourapp/payment.html', {
        'package': package,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    })
@login_required
def vendor_dashboard(request):
    if not hasattr(request.user, 'vendor'):
        return redirect('home')

    vendor_packages = Package.objects.filter(vendor=request.user.vendor)
    vendor_bookings = Booking.objects.filter(package__vendor=request.user.vendor)
    bookings = Booking.objects.filter(package__in=vendor_packages).select_related('user', 'package')
    return render(request, 'tourapp/vendor_dashboard.html', {
        'packages': vendor_packages,
        'bookings': bookings
    })



@staff_member_required
def admin_package_approval(request):
    pending_packages = Package.objects.filter(is_approved=False)
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        action = request.POST.get('action')
        package = Package.objects.get(id=package_id)
        if action == 'approve':
            package.is_approved = True
            package.save()
        elif action == 'reject':
            package.delete()
        return redirect('admin_package_approval')

    return render(request, 'tourapp/admin_package_approval.html', {'packages': pending_packages})

