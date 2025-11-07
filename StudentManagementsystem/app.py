from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import init_db, get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

init_db()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if user_type == 'admin':
            conn = get_db_connection()
            admin = conn.execute('SELECT * FROM admin WHERE username = ?', (username,)).fetchone()
            conn.close()
            
            if admin and check_password_hash(admin['password'], password):
                session['user_id'] = admin['id']
                session['username'] = admin['username']
                session['user_type'] = 'admin'
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials', 'error')
        
        elif user_type == 'student':
            conn = get_db_connection()
            student = conn.execute('SELECT * FROM students WHERE student_id = ?', (username,)).fetchone()
            conn.close()
            
            if student and check_password_hash(student['password'], password):
                session['user_id'] = student['id']
                session['username'] = student['student_id']
                session['user_type'] = 'student'
                session['student_name'] = student['name']
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid student credentials', 'error')
    
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    total_students = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    total_courses = conn.execute('SELECT COUNT(*) FROM courses').fetchone()[0]
    
    fee_stats = conn.execute('''
        SELECT 
            COUNT(*) as total_records,
            SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) as paid_count,
            SUM(CASE WHEN payment_status = 'unpaid' THEN 1 ELSE 0 END) as unpaid_count,
            SUM(amount) as total_amount,
            SUM(CASE WHEN payment_status = 'paid' THEN amount ELSE 0 END) as paid_amount
        FROM fee_records
    ''').fetchone()
    
    recent_students = conn.execute('''
        SELECT s.*, c.course_name 
        FROM students s 
        LEFT JOIN courses c ON s.course_id = c.id 
        ORDER BY s.created_at DESC LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         total_students=total_students,
                         total_courses=total_courses,
                         fee_stats=fee_stats,
                         recent_students=recent_students)

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    student = conn.execute('''
        SELECT s.*, c.course_name, c.fee_amount 
        FROM students s 
        LEFT JOIN courses c ON s.course_id = c.id 
        WHERE s.id = ?
    ''', (session['user_id'],)).fetchone()
    
    today_attendance = conn.execute('''
        SELECT status FROM attendance 
        WHERE student_id = ? AND attendance_date = DATE('now')
    ''', (session['user_id'],)).fetchone()
    
    attendance_summary = conn.execute('''
        SELECT 
            COUNT(*) as total_days,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_days
        FROM attendance 
        WHERE student_id = ? AND strftime('%Y-%m', attendance_date) = strftime('%Y-%m', 'now')
    ''', (session['user_id'],)).fetchone()
    
    fee_status = conn.execute('''
        SELECT payment_status, amount, due_date 
        FROM fee_records 
        WHERE student_id = ? AND semester = ?
        ORDER BY created_at DESC LIMIT 1
    ''', (session['user_id'], student['semester'])).fetchone()
    
    conn.close()
    
    return render_template('student_dashboard.html', 
                         student=student,
                         today_attendance=today_attendance,
                         attendance_summary=attendance_summary,
                         fee_status=fee_status)

@app.route('/admin/courses')
def manage_courses():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('manage_courses.html', courses=courses)

@app.route('/admin/courses/add', methods=['GET', 'POST'])
def add_course():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        fee_amount = request.form['fee_amount']
        duration = request.form['duration']
        description = request.form['description']
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO courses (course_code, course_name, fee_amount, duration, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (course_code, course_name, fee_amount, duration, description))
            conn.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('manage_courses'))
        except sqlite3.IntegrityError:
            flash('Course code already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('add_course.html')

@app.route('/admin/courses/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        fee_amount = request.form['fee_amount']
        duration = request.form['duration']
        description = request.form['description']
        
        try:
            conn.execute('''
                UPDATE courses 
                SET course_code = ?, course_name = ?, fee_amount = ?, duration = ?, description = ?
                WHERE id = ?
            ''', (course_code, course_name, fee_amount, duration, description, id))
            conn.commit()
            flash('Course updated successfully!', 'success')
            return redirect(url_for('manage_courses'))
        except sqlite3.IntegrityError:
            flash('Course code already exists!', 'error')
    
    course = conn.execute('SELECT * FROM courses WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if not course:
        flash('Course not found!', 'error')
        return redirect(url_for('manage_courses'))
    
    return render_template('edit_course.html', course=course)

@app.route('/admin/courses/delete/<int:id>')
def delete_course(id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    students_count = conn.execute('SELECT COUNT(*) FROM students WHERE course_id = ?', (id,)).fetchone()[0]
    
    if students_count > 0:
        flash('Cannot delete course. There are students enrolled in this course.', 'error')
    else:
        conn.execute('DELETE FROM courses WHERE id = ?', (id,))
        conn.commit()
        flash('Course deleted successfully!', 'success')
    
    conn.close()
    return redirect(url_for('manage_courses'))

@app.route('/admin/students')
def manage_students():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    students = conn.execute('''
        SELECT s.*, c.course_name, c.fee_amount 
        FROM students s 
        LEFT JOIN courses c ON s.course_id = c.id 
        ORDER BY s.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('manage_students.html', students=students)

@app.route('/admin/students/add', methods=['GET', 'POST'])
def add_student():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses ORDER BY course_name').fetchall()
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course_id = request.form['course_id']
        semester = request.form['semester']
        
        from database import generate_student_password
        temp_password = generate_student_password()
        password = generate_password_hash(temp_password)
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (student_id, name, email, phone, course_id, semester, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, name, email, phone, course_id, semester, password))
            
            student_db_id = cursor.lastrowid
            
            course_fee = conn.execute('SELECT fee_amount FROM courses WHERE id = ?', (course_id,)).fetchone()
            if course_fee:
                due_date = date.today() + timedelta(days=30)  
                conn.execute('''
                    INSERT INTO fee_records (student_id, course_id, semester, amount, payment_status, due_date)
                    VALUES (?, ?, ?, ?, 'unpaid', ?)
                ''', (student_db_id, course_id, semester, course_fee['fee_amount'], due_date))
            
            conn.commit()
            
            session['new_student_temp_password'] = {
                'student_id': student_id,
                'temp_password': temp_password,
                'name': name
            }
            
            flash('Student added successfully! Temporary password generated.', 'success')
            return redirect(url_for('show_temp_password'))
        except sqlite3.IntegrityError as e:
            flash('Student ID or Email already exists!', 'error')
        finally:
            conn.close()
    else:
        conn.close()
    
    return render_template('add_student.html', courses=courses)

@app.route('/admin/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM courses ORDER BY course_name').fetchall()
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course_id = request.form['course_id']
        semester = request.form['semester']
        
        try:
            conn.execute('''
                UPDATE students 
                SET student_id = ?, name = ?, email = ?, phone = ?, course_id = ?, semester = ?
                WHERE id = ?
            ''', (student_id, name, email, phone, course_id, semester, id))
            conn.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('manage_students'))
        except sqlite3.IntegrityError:
            flash('Student ID or Email already exists!', 'error')
    
    student = conn.execute('''
        SELECT s.*, c.course_name 
        FROM students s 
        LEFT JOIN courses c ON s.course_id = c.id 
        WHERE s.id = ?
    ''', (id,)).fetchone()
    
    conn.close()
    
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('manage_students'))
    
    return render_template('edit_student.html', student=student, courses=courses)

@app.route('/admin/students/delete/<int:id>')
def delete_student(id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    conn.execute('DELETE FROM attendance WHERE student_id = ?', (id,))
    conn.execute('DELETE FROM fee_records WHERE student_id = ?', (id,))
    
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('manage_students'))

@app.route('/admin/students/reset-password/<int:id>', methods=['GET', 'POST'])
def reset_student_password(id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    student = conn.execute('''
        SELECT s.*, c.course_name 
        FROM students s 
        LEFT JOIN courses c ON s.course_id = c.id 
        WHERE s.id = ?
    ''', (id,)).fetchone()
    
    if request.method == 'POST':
        from database import generate_student_password
        temp_password = generate_student_password()
        password = generate_password_hash(temp_password)
        
        conn.execute('UPDATE students SET password = ? WHERE id = ?', (password, id))
        conn.commit()
        conn.close()
        
        session['reset_student_temp_password'] = {
            'student_id': student['student_id'],
            'temp_password': temp_password,
            'name': student['name']
        }
        
        flash('Password reset successfully! New temporary password generated.', 'success')
        return redirect(url_for('show_reset_password'))
    
    conn.close()
    
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('manage_students'))
    
    return render_template('reset_password_confirm.html', student=student)

@app.route('/admin/students/temp-password')
def show_temp_password():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if 'new_student_temp_password' not in session:
        return redirect(url_for('manage_students'))
    
    temp_password_info = session.pop('new_student_temp_password', None)
    
    return render_template('temp_password.html', temp_password_info=temp_password_info)

@app.route('/admin/students/reset-password-result')
def show_reset_password():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if 'reset_student_temp_password' not in session:
        return redirect(url_for('manage_students'))
    
    temp_password_info = session.pop('reset_student_temp_password', None)
    
    return render_template('temp_password.html', temp_password_info=temp_password_info)

@app.route('/student/attendance', methods=['GET', 'POST'])
def student_attendance():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        status = request.form['status'] 
        
        try:
            conn.execute('''
                INSERT OR REPLACE INTO attendance (student_id, attendance_date, status)
                VALUES (?, DATE('now'), ?)
            ''', (session['user_id'], status))
            conn.commit()
            flash(f'Attendance marked as {status} for today!', 'success')
        except sqlite3.Error as e:
            flash('Error marking attendance. Please try again.', 'error')
    
    today_attendance = conn.execute('''
        SELECT status FROM attendance 
        WHERE student_id = ? AND attendance_date = DATE('now')
    ''', (session['user_id'],)).fetchone()
    
    attendance_history = conn.execute('''
        SELECT attendance_date, status 
        FROM attendance 
        WHERE student_id = ? 
        AND attendance_date >= DATE('now', '-30 days')
        ORDER BY attendance_date DESC
    ''', (session['user_id'],)).fetchall()
    
    attendance_summary = conn.execute('''
        SELECT 
            COUNT(*) as total_days,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_days,
            SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_days
        FROM attendance 
        WHERE student_id = ? AND strftime('%Y-%m', attendance_date) = strftime('%Y-%m', 'now')
    ''', (session['user_id'],)).fetchone()
    
    conn.close()
    
    return render_template('student_attendance.html',
                         today_attendance=today_attendance,
                         attendance_history=attendance_history,
                         attendance_summary=attendance_summary)

@app.route('/admin/attendance')
def admin_attendance():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    date_filter = request.args.get('date', date.today().isoformat())
    
    conn = get_db_connection()
    
    attendance_data = conn.execute('''
        SELECT s.student_id, s.name, c.course_name, a.status
        FROM students s
        LEFT JOIN courses c ON s.course_id = c.id
        LEFT JOIN attendance a ON s.id = a.student_id AND a.attendance_date = ?
        ORDER BY s.name
    ''', (date_filter,)).fetchall()
    
    conn.close()
    
    return render_template('admin_attendance.html',
                         attendance_data=attendance_data,
                         selected_date=date_filter)

@app.route('/admin/fees')
def manage_fees():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    status_filter = request.args.get('status', 'all')
    
    conn = get_db_connection()
    
    if status_filter == 'all':
        fee_records = conn.execute('''
            SELECT fr.*, s.student_id, s.name, s.semester, c.course_name
            FROM fee_records fr
            JOIN students s ON fr.student_id = s.id
            JOIN courses c ON fr.course_id = c.id
            ORDER BY fr.created_at DESC
        ''').fetchall()
    else:
        fee_records = conn.execute('''
            SELECT fr.*, s.student_id, s.name, s.semester, c.course_name
            FROM fee_records fr
            JOIN students s ON fr.student_id = s.id
            JOIN courses c ON fr.course_id = c.id
            WHERE fr.payment_status = ?
            ORDER BY fr.created_at DESC
        ''', (status_filter,)).fetchall()
    
    conn.close()
    
    return render_template('manage_fees.html', fee_records=fee_records, status_filter=status_filter)

@app.route('/admin/fees/update_status/<int:fee_id>', methods=['POST'])
def update_fee_status(fee_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    try:
        payment_status = request.form.get('payment_status')
        
        if not payment_status:
            flash('Payment status is required!', 'error')
            return redirect(url_for('manage_fees'))
        
        if payment_status not in ['paid', 'unpaid']:
            flash('Invalid payment status!', 'error')
            return redirect(url_for('manage_fees'))
        
        conn = get_db_connection()
        
        if payment_status == 'paid':
            conn.execute('''
                UPDATE fee_records 
                SET payment_status = ?, payment_date = DATE('now')
                WHERE id = ?
            ''', (payment_status, fee_id))
        else:
            conn.execute('''
                UPDATE fee_records 
                SET payment_status = ?, payment_date = NULL
                WHERE id = ?
            ''', (payment_status, fee_id))
        
        conn.commit()
        conn.close()
        
        flash('Fee status updated successfully!', 'success')
        return redirect(url_for('manage_fees'))
    
    except Exception as e:
        flash('Error updating fee status. Please try again.', 'error')
        return redirect(url_for('manage_fees'))

@app.route('/student/fees')
def student_fees():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    student_course = conn.execute('''
        SELECT c.course_name, c.fee_amount, s.semester
        FROM students s
        JOIN courses c ON s.course_id = c.id
        WHERE s.id = ?
    ''', (session['user_id'],)).fetchone()
    
    fee_history = conn.execute('''
        SELECT semester, amount, payment_status, payment_date, due_date, created_at
        FROM fee_records
        WHERE student_id = ?
        ORDER BY semester DESC, created_at DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    return render_template('student_fees.html',
                         student_course=student_course,
                         fee_history=fee_history)

@app.route('/student/profile')
def student_profile():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    student = conn.execute('''
        SELECT s.*, c.course_name, c.fee_amount 
        FROM students s 
        LEFT JOIN courses c ON s.course_id = c.id 
        WHERE s.id = ?
    ''', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('view_students.html', student=student)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)