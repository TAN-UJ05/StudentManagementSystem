# Student Management System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

A comprehensive **web-based Student Management System** built with Flask and SQLite3 that provides separate interfaces for administrators and students with full CRUD operations, attendance tracking, and fee management.

---

## ✨ Features

### 👨‍💼 Admin Panel
| Feature | Description |
|---------|-------------|
| 📊 **Dashboard** | System statistics and recent activities overview |
| 👥 **Student Management** | Add, view, edit, and delete student records |
| 📚 **Course Management** | Create and manage courses with fee structures |
| 💰 **Fee Management** | Track and update student fee payments |
| 📅 **Attendance Monitoring** | View student attendance records |
| 🔐 **Password Reset** | Reset student passwords with temporary credentials |

### 👨‍🎓 Student Panel
| Feature | Description |
|---------|-------------|
| 🏠 **Personal Dashboard** | Overview of attendance and fees |
| ✅ **Attendance Marking** | Mark daily attendance (present/absent) |
| 💳 **Fee Viewing** | View course fees and payment history |
| 👤 **Profile Management** | View personal information and course details |

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python Web Framework)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Authentication**: Session-based with password hashing
- **Security**: Werkzeug security utilities
- **Templating**: Jinja2

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd StudentManagementSystem
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

---

## 🔐 Default Login Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

### Student Accounts
- Students are created by admin with auto-generated temporary passwords
- Students use their **Student ID** as username

---

## 📁 Project Structure

```
StudentManagementSystem/
│
├── 📄 app.py                          # Main Flask application
├── 📄 database.py                     # Database configuration
├── 📄 requirements.txt                # Python dependencies
│
├── 📁 static/
│   └── 📁 css/
│       └── 📄 style.css              # Custom styles
│
└── 📁 templates/
    │
    ├── 📄 base.html                   # Base layout template
    ├── 📄 login.html                  # Login page
    │
    ├── 📁 admin/                      # Admin panel templates
    │   │
    │   ├── 📄 dashboard.html          # Admin dashboard (renamed from admin_dashboard.html)
    │   │
    │   ├── 📁 students/               # Student management
    │   │   ├── 📄 manage.html         # Manage students (renamed from manage_students.html)
    │   │   ├── 📄 add.html            # Add student (renamed from add_student.html)
    │   │   ├── 📄 edit.html           # Edit student (renamed from edit_student.html)
    │   │   └── 📄 temp_password.html  # Temporary password display
    │   │
    │   ├── 📁 courses/                # Course management
    │   │   ├── 📄 manage.html         # Manage courses (renamed from manage_courses.html)
    │   │   ├── 📄 add.html            # Add course (renamed from add_course.html)
    │   │   └── 📄 edit.html           # Edit course (renamed from edit_course.html)
    │   │
    │   ├── 📁 fees/                   # Fee management
    │   │   └── 📄 manage.html         # Manage fees (renamed from manage_fees.html)
    │   │
    │   └── 📁 attendance/             # Attendance management
    │       └── 📄 view.html           # View attendance (renamed from admin_attendance.html)
    │
    ├── 📁 student/                    # Student panel templates
    │   │
    │   ├── 📄 dashboard.html          # Student dashboard (renamed from student_dashboard.html)
    │   ├── 📄 profile.html            # Student profile (renamed from view_students.html)
    │   ├── 📄 attendance.html         # Student attendance (renamed from student_attendance.html)
    │   └── 📄 fees.html               # Student fees (renamed from student_fees.html)
    │
    └── 📁 shared/                     # Shared templates
        └── 📄 reset_password_confirm.html  # Password reset confirmation

```

---

## 🗃️ Database Schema

| Table | Description |
|-------|-------------|
| **admin** | Administrator accounts |
| **students** | Student information and credentials |
| **courses** | Course details and fee structures |
| **attendance** | Daily student attendance records |
| **fee_records** | Student fee payment records |

---

## 💻 Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Create Courses** first before adding students
3. **Add Students** and assign them to courses
4. **Manage Fees** by updating payment status
5. **Monitor Attendance** by viewing attendance records

### For Students

1. **Login** with Student ID and password
2. **Mark Attendance** daily
3. **View Fees** and payment status
4. **Check Profile** for personal and course information

---

## 🎯 API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/students` - Manage students
- `GET/POST /admin/students/add` - Add new student
- `GET/POST /admin/students/edit/<id>` - Edit student
- `GET /admin/students/delete/<id>` - Delete student
- `GET /admin/courses` - Manage courses
- `GET/POST /admin/courses/add` - Add new course
- `GET/POST /admin/courses/edit/<id>` - Edit course
- `GET /admin/courses/delete/<id>` - Delete course
- `GET /admin/fees` - Manage fees
- `POST /admin/fees/update_status/<fee_id>` - Update fee status
- `GET /admin/attendance` - View attendance

### Student Routes
- `GET /student/dashboard` - Student dashboard
- `GET /student/profile` - Student profile
- `GET/POST /student/attendance` - Mark/view attendance
- `GET /student/fees` - View fee details

---

## 🔒 Security Features

- 🔐 **Password Hashing** using Werkzeug
- 🛡️ **Session-based Authentication**
- 👥 **Role-based Access Control** (Admin/Student)
- 🚫 **SQL Injection Prevention** through parameterized queries
- 🔑 **Secure Temporary Password** generation

---

## 🐛 Troubleshooting

### Common Issues

1. **Database not created**
   - Ensure write permissions in the project directory
   - Check if SQLite3 is properly installed

2. **Login issues**
   - Verify default admin credentials
   - Check if student exists in the database

3. **Template errors**
   - Ensure all required template files are present
   - Check template file paths in `app.py`

4. **Port already in use**
   ```bash
   # Kill the process using port 5000
   sudo lsof -t -i tcp:5000 | xargs kill -9
   ```

---

## 🚀 Future Enhancements

- 📧 Email notifications for students
- 🔄 Student self-password change feature
- 📈 Advanced reporting and analytics
- 📥 Bulk student import/export
- 📱 Mobile-responsive improvements
- 💳 Payment gateway integration
- 🗓️ Academic calendar integration

---

## 📋 Complete File List

### Required Files:

#### Core Application
- `app.py` - Main Flask application
- `database.py` - Database configuration
- `requirements.txt` - Dependencies

#### Templates
- `templates/base.html` - Base layout template
- `templates/login.html` - Login page

#### Admin Templates
- `templates/admin/dashboard.html` - Admin dashboard
- `templates/admin/students/manage.html` - Manage students
- `templates/admin/students/add.html` - Add student
- `templates/admin/students/edit.html` - Edit student
- `templates/admin/students/temp_password.html` - Temporary password
- `templates/admin/courses/manage.html` - Manage courses
- `templates/admin/courses/add.html` - Add course
- `templates/admin/courses/edit.html` - Edit course
- `templates/admin/fees/manage.html` - Manage fees
- `templates/admin/attendance/view.html` - View attendance

#### Student Templates
- `templates/student/dashboard.html` - Student dashboard
- `templates/student/profile.html` - Student profile
- `templates/student/attendance.html` - Student attendance
- `templates/student/fees.html` - Student fees

#### Shared Templates
- `templates/shared/reset_password_confirm.html` - Password reset

#### Static Files
- `static/css/style.css` - Custom styles

---

## 🛠️ Development Setup

### Step-by-Step Installation:

1. **Extract all files to a folder**
2. **Open terminal/command prompt in that folder**
3. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the application:**
   ```bash
   python app.py
   ```
6. **Open browser and go to: `http://localhost:5000`**

### Dependencies (requirements.txt):
```
Flask==2.3.3
Werkzeug==2.3.7
```

---

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all files are in the correct directory structure
3. Verify Python version is 3.8+
4. Check that all dependencies are installed

---

## 👥 Authors

- **Tanuj Joshi** - Initial development

## 📫 Contact

- **GitHub:** https://github.com/TAN-UJ05
- **Email:** tanujjoshi669@gmail.com

---

## ⚖️ License

MIT License  
Made with ❤️ using Python and Flask.
