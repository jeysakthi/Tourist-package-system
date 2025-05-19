Here is a **short project documentation** for your **Tour Packages Management System** along with the GitHub repository link.

---

### 🧾 **Project Documentation: Tour Packages Management System**

---

#### 📌 Project Title:

**Tour Packages Management System**

---

#### 📝 Project Description:

The **Tour Packages Management System** is a web-based application developed using **Django**, **HTML/CSS**, and **TailwindCSS**. It aims to simplify the process of booking and managing tour packages for users, vendors, and administrators. The system supports user registration, package browsing, booking, payment through Razorpay, and role-based dashboards for vendors and admin users.

---

#### 🎯 Objectives:

* Allow users to browse and book tour packages easily.
* Enable vendors to add, edit, and manage their packages.
* Provide an admin panel to oversee users, vendors, and bookings.
* Integrate a secure and responsive online payment gateway using Razorpay.

---

#### 🔧 Technologies Used:

* **Frontend**: HTML, CSS, TailwindCSS, JavaScript
* **Backend**: Django (Python)
* **Database**: SQLite (default Django DB)
* **Payment Integration**: Razorpay API
* **Animation Library**: AOS (Animate On Scroll)

---

#### 👤 User Roles:

* **User**: Can register, browse packages, book, and make payments.
* **Vendor**: Can add/edit/delete their tour packages.
* **Admin**: Full access to manage users, vendors, and packages.

---

#### 💡 Key Features:

* Role-based login system (User, Vendor, Admin)
* Beautiful and responsive UI using Tailwind CSS
* Booking confirmation and history tracking
* Razorpay payment gateway integration
* Email notifications for booking confirmations (optional)
* Dashboard for all user types

---

#### 💻 Installation & Setup:

1. Clone the repository:

   ```bash
   git clone https://github.com/jeysakthi/Tourist-package-system.git
   cd Tourist-package-system
   ```
2. Create a virtual environment and activate it:

   ```bash
   python -m venv env
   source env/bin/activate  # on Windows use `env\Scripts\activate`
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:

   ```bash
   python manage.py migrate
   ```
5. Run the development server:

   ```bash
   python manage.py runserver
   ```

---

#### 🔗 GitHub Repository:

📁 [Final Project Source Code – GitHub](https://github.com/jeysakthi/Tourist-package-system/tree/master)
