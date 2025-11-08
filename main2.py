import pyodbc
from datetime import datetime
import time

def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=LAPTOP-TQG52AHM\SQLEXPRESS;'
    'Database=university_portal;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def add_department():
    name=input("Department name : ")
    building=input("Department building : ")
    cursor.execute("INSERT INTO Departments(name,building) VALUES(?,?)",
                   (name,building))
    conn.commit()

def display_departments():
    cursor.execute("SELECT * FROM Departments")
    result = cursor.fetchall()
    
    if result:
        print(f"{'ID':<5} {'Name':<20} {'Building':<15}")
        print("-" * 45)
        for row in result:
            dept_id, name, building = row
            print(f"{dept_id:<5} {name:<20} {building:<15}")
    else:
        print("No departments found in the system.")


def stu_in_dep():
    cursor.execute("""
        SELECT COUNT(s.student_id) AS Total_students, d.name AS Department_name
        FROM Students s
        INNER JOIN Departments d ON s.department_id = d.department_id
        GROUP BY d.name;
    """)
    
    result = cursor.fetchall()
    
    if result:
        print("\nStudents per Department:")
        for row in result:
            print(f"Department: {row.Department_name}, Total Students: {row.Total_students}")
    else:
        print("No departments found in the system.")


def delete_department():
    department_id = int(input("Enter the department ID to delete: "))
    
    cursor.execute("DELETE FROM Departments WHERE department_id = ?", (department_id,))
    conn.commit()
    print("Department deleted successfully.")

def update_department():
    department_id = int(input("Enter the department ID to update: "))
    cursor.execute("SELECT * FROM Departments WHERE department_id = ?", (department_id,))
    result = cursor.fetchone()

    if result is None:
        print("Department ID not found.")
        return
    new_name = input("New Department Name: ")
    new_building = input("New Building: ")
    
    cursor.execute("""
        UPDATE Departments
        SET name = ?, building = ?
        WHERE department_id = ?
    """, (new_name, new_building, department_id))
    
    conn.commit()
    print("Department updated successfully.")


def add_student():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone = input("Phone (optional): ") or None
    date_of_birth = get_valid_date("Date of Birth (YYYY-MM-DD): ")
    department_id = int(input("Department ID: "))
    enrollment_date = get_valid_date("Enrollment Date (YYYY-MM-DD): ")

    cursor.execute("""
        INSERT INTO Students (
            first_name, last_name, email, phone, date_of_birth, department_id, enrollment_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, email, phone, date_of_birth, department_id, enrollment_date))

    conn.commit()
    print("Student added successfully.")

def display_students():
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()

    if students:
        print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Phone':<15} {'DOB':<12} {'Dept ID':<8} {'Enroll Date':<12}")
        print("-" * 120)
        for s in students:
            print(f"{s[0]:<5} {s[1]:<15} {s[2]:<15} {s[3]:<30} {s[4]:<15} {str(s[5]):<12} {s[6]:<8} {str(s[7]):<12}")
    else:
        print("No students found in the system.")


def delete_student():
    student_id = int(input("Enter the student ID to delete: "))
    
    cursor.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
    conn.commit()
    print("Student deleted successfully.")

def update_student():
    student_id = int(input("Enter the student ID to update: "))
    cursor.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
    result = cursor.fetchone()

    if result is None:
        print("Student ID not found.")
        return
    new_first_name = input("New First Name: ")
    new_last_name = input("New Last Name: ")
    new_email = input("New Email: ")
    new_phone = input("New Phone (optional): ") or None
    new_date_of_birth = get_valid_date("New Date of Birth (YYYY-MM-DD): ")
    new_department_id = int(input("New Department ID: "))
    
    cursor.execute("""
        UPDATE Students
        SET first_name = ?, last_name = ?, email = ?, phone = ?, date_of_birth = ?, department_id = ?
        WHERE student_id = ?
    """, (new_first_name, new_last_name, new_email, new_phone, new_date_of_birth, new_department_id, student_id))
    
    conn.commit()
    print("Student updated successfully.")

def display_deleted_students():
    cursor.execute("SELECT * FROM Deleted_students")
    deleted_students = cursor.fetchall()
    
    if deleted_students:
        print("Deleted Students:")
        for student in deleted_students:
            print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, Email: {student.email}, Phone: {student.phone}, DOB: {student.date_of_birth}, Department ID: {student.department_id}, Enrollment Date: {student.enrollment_date}")
    else:
        print("No students have been deleted.")

def add_teacher():
    name=input("Name : ")
    email = input("Email: ")
    dep_id=int(input("Department id : "))
    hire=get_valid_date("Hire Date (YYYY-MM-DD): ")

    cursor.execute("INSERT INTO FacultyMember(name,email,department_id,hire_date) VALUES (?,?,?,?)",
                   (name,email,dep_id,hire))
    conn.commit()
    print("Faculty member added successfully")

def display_teachers():
    cursor.execute("SELECT * FROM FacultyMember")
    teachers = cursor.fetchall()

    if teachers:
        print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Dept ID':<10} {'Hire Date':<12}")
        print("-" * 90)
        for t in teachers:
            print(f"{t[0]:<5} {t[1]:<25} {t[2]:<30} {t[3]:<10} {str(t[4]):<12}")
    else:
        print("No faculty members found.")

def faculty_in_department():
    cursor.execute("""
        SELECT 
            f.faculty_id,
            f.name AS Faculty_Name,
            d.name AS Department_Name
        FROM 
            FacultyMember f
        INNER JOIN 
            Departments d ON f.department_id = d.department_id;
    """)
    rows = cursor.fetchall()

    if rows:
        print(f"{'Faculty ID':<12} {'Faculty Name':<25} {'Department':<25}")
        print("-" * 65)
        for r in rows:
            print(f"{r[0]:<12} {r[1]:<25} {r[2]:<25}")
    else:
        print("No faculty data found.")

def delete_faculty_member():
    faculty_id = int(input("Enter the faculty member ID to delete: "))
    
    # Deleting the faculty member will automatically trigger the insertion into the Deleted_faculty_members table.
    cursor.execute("DELETE FROM FacultyMember WHERE faculty_id = ?", (faculty_id,))
    conn.commit()
    print("Faculty member deleted successfully.")
    
def update_faculty_member():
    faculty_id = int(input("Enter the faculty member ID to update: "))
    cursor.execute("SELECT * FROM FacultyMember WHERE faculty_id = ?", (faculty_id,))
    result = cursor.fetchone()

    if result is None:
        print("Faculty Member ID not found.")
        return
    new_name = input("New Name: ")
    new_email = input("New Email: ")
    new_department_id = int(input("New Department ID: "))
    new_hire_date = get_valid_date("New Hire Date (YYYY-MM-DD): ")
    
    cursor.execute("""
        UPDATE FacultyMember
        SET name = ?, email = ?, department_id = ?, hire_date = ?
        WHERE faculty_id = ?
    """, (new_name, new_email, new_department_id, new_hire_date, faculty_id))
    
    conn.commit()
    print("Faculty member updated successfully.")

def display_deleted_faculty_members():
    cursor.execute("SELECT * FROM Deleted_faculty_members")
    dfm = cursor.fetchall()

    if dfm:
        print("Deleted Faculty Members:")
        print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Dept ID':<10} {'Hire Date':<12}")
        print("-" * 90)
        for f in dfm:
            print(f"{f[0]:<5} {f[1]:<25} {f[2]:<30} {f[3]:<10} {str(f[4]):<12}")
    else:
        print("No deleted faculty members found.")


def add_course():
    name = input("Course Name: ")
    credits = int(input("Credits: "))
    department_id = int(input("Department ID: "))
    faculty_id = int(input("Faculty Member ID: "))

    cursor.execute("""
        INSERT INTO Courses (name, credits, department_id, faculty_id)
        VALUES (?, ?, ?, ?)
    """, (name, credits, department_id, faculty_id))

    conn.commit()
    print("Course added successfully.")

def display_courses():
    cursor.execute("SELECT * FROM Courses")
    courses = cursor.fetchall()

    if courses:
        print(f"{'ID':<5} {'Name':<30} {'Credits':<8} {'Dept ID':<10} {'Faculty ID':<12}")
        print("-" * 75)
        for c in courses:
            print(f"{c[0]:<5} {c[1]:<30} {c[2]:<8} {c[3]:<10} {c[4]:<12}")
    else:
        print("No courses found.")


def students_in_courses():
    course_name = input("Enter course name: ")

    cursor.execute("SELECT COUNT(*) FROM Courses WHERE LOWER(name) = LOWER(?)", (course_name,))
    course_exists = cursor.fetchone()[0]

    if course_exists:
        cursor.execute("EXEC students_in_courses @course_name=?", (course_name,))
        results = cursor.fetchall()

        if results:
            print(f"\nStudents enrolled in '{course_name}':")
            print(f"\n{'Student ID':<12} {'Student Name':<30}")
            print("-" * 45)
            for row in results:
                print(f"{row.student_id:<12} {row.Student_Name:<30}")
        else:
            print(f"No students found enrolled in '{course_name}'.")
    else:
        print(f"The course '{course_name}' does not exist in the system.")

def delete_course():
    course_id = int(input("Enter the course ID to delete: "))
    
    cursor.execute("DELETE FROM Courses WHERE course_id = ?", (course_id,))
    conn.commit()
    print("Course deleted successfully.")

def update_course():
    course_id = int(input("Enter the course ID to update: "))
    cursor.execute("SELECT * FROM Courses WHERE course_id = ?", (course_id,))
    result = cursor.fetchone()

    if result is None:
        print("Course ID not found.")
        return
    new_name = input("New Course Name: ")
    new_credits = int(input("New Credits: "))
    new_department_id = int(input("New Department ID: "))
    new_faculty_id = int(input("New Faculty Member ID: "))
    
    cursor.execute("""
        UPDATE Courses
        SET name = ?, credits = ?, department_id = ?, faculty_id = ?
        WHERE course_id = ?
    """, (new_name, new_credits, new_department_id, new_faculty_id, course_id))
    
    conn.commit()
    print("Course updated successfully.")

def add_enrollment():
    student_id = int(input("Student ID: "))
    course_id = int(input("Course ID: "))
    enrolled_on = get_valid_date("Enrolled On (YYYY-MM-DD): ")
    semester = input("Semester (e.g., Fall 2025): ")

    cursor.execute("""
        INSERT INTO Enrollments (student_id, course_id, enrolled_on, semester)
        VALUES (?, ?, ?, ?)
    """, (student_id, course_id, enrolled_on, semester))

    conn.commit()
    print("Enrollment added successfully.")

def show_enrollments():
    cursor.execute("""
        SELECT 
            e.enrollment_id,
            s.first_name + ' ' + s.last_name AS Student_Name,
            c.name AS Course_Name,
            e.semester,
            e.enrolled_on
        FROM Enrollments e
        INNER JOIN Students s ON e.student_id = s.student_id
        INNER JOIN Courses c ON e.course_id = c.course_id;
    """)
    rows = cursor.fetchall()

    if rows:
        print(f"{'Enroll ID':<10} {'Student Name':<25} {'Course':<25} {'Semester':<10} {'Enrolled On':<12}")
        print("-" * 90)
        for r in rows:
            print(f"{r[0]:<10} {r[1]:<25} {r[2]:<25} {r[3]:<10} {str(r[4]):<12}")
    else:
        print("No enrollments found.")

def delete_enrollment():
    enrollment_id = int(input("Enter the enrollment ID to delete: "))
    
    cursor.execute("DELETE FROM Enrollments WHERE enrollment_id = ?", (enrollment_id,))
    conn.commit()
    print("Enrollment deleted successfully.")

def update_enrollment():
    enrollment_id = int(input("Enter the enrollment ID to update: "))
    cursor.execute("SELECT * FROM Enrollments WHERE enrollment_id = ?", (enrollment_id,))
    result = cursor.fetchone()

    if result is None:
        print("Enrollment ID not found.")
        return
    new_student_id = int(input("New Student ID: "))
    new_course_id = int(input("New Course ID: "))
    new_enrolled_on = get_valid_date("New Enrollment Date (YYYY-MM-DD): ")
    new_semester = input("New Semester: ")
    
    cursor.execute("""
        UPDATE Enrollments
        SET student_id = ?, course_id = ?, enrolled_on = ?, semester = ?
        WHERE enrollment_id = ?
    """, (new_student_id, new_course_id, new_enrolled_on, new_semester, enrollment_id))
    
    conn.commit()
    print("Enrollment updated successfully.")

def add_grade():
    enrollment_id = int(input("Enrollment ID: "))
    term=input("Term : ")
    grade = input("Grade (e.g., A+, B): ")
    remarks = input("Remarks (optional): ") or None

    cursor.execute("""
        INSERT INTO Grades (enrollment_id,term, grade, remarks)
        VALUES (?, ?, ?, ?)
    """, (enrollment_id,term,grade, remarks))

    conn.commit()
    print("Grade added successfully.")

def show_student_grades():
    course_name = input("Enter course name: ")
    cursor.execute("SELECT COUNT(*) FROM Courses WHERE LOWER(name) = LOWER(?)", (course_name,))
    course_exists = cursor.fetchone()[0]
    
    if course_exists:
        cursor.execute("""
        SELECT 
            s.first_name + ' ' + s.last_name AS Student_Name,
            c.name AS Course_Name,
            g.term AS Term,
            g.grade AS Grade,
            g.remarks AS Remarks
        FROM 
            Grades g
        INNER JOIN Enrollments e ON g.enrollment_id = e.enrollment_id
        INNER JOIN Students s ON e.student_id = s.student_id
        INNER JOIN Courses c ON e.course_id = c.course_id
        WHERE LOWER(c.name) = LOWER(?);
        """, (course_name,))
    
        results = cursor.fetchall()
        if results:
            print(f"{'Student Name':<25} {'Course':<25} {'Term':<10} {'Grade':<8} {'Remarks'}")
            print("-" * 80)
            for row in results:
                print(f"{row[0]:<25} {row[1]:<25} {row[2]:<10} {row[3]:<8} {row[4]}")
        else:
            print(f"No grades found for the course: {course_name}")
    else:
        print(f"The course '{course_name}' does not exist in the system.")

def delete_grade():
    grade_id = int(input("Enter the grade ID to delete: "))
    
    cursor.execute("DELETE FROM Grades WHERE grade_id = ?", (grade_id,))
    conn.commit()
    print("Grade deleted successfully.")

def update_grade():
    grade_id = int(input("Enter the grade ID to update: "))
    cursor.execute("SELECT * FROM Grades WHERE grade_id = ?", (grade_id,))
    result = cursor.fetchone()

    if result is None:
        print("Grade ID not found.")
        return
    new_term = input("New Term (e.g., Midterm, Final): ")
    new_grade = input("New Grade: ")
    new_remarks = input("New Remarks (optional): ") or None
    
    cursor.execute("""
        UPDATE Grades
        SET term = ?, grade = ?, remarks = ?
        WHERE grade_id = ?
    """, (new_term, new_grade, new_remarks, grade_id))
    
    conn.commit()
    print("Grade updated successfully.")

def add_attendance():
    student_id = int(input("Student ID: "))
    course_id = int(input("Course ID: "))
    date = get_valid_date("Date (YYYY-MM-DD): ")
    status = input("Status (Present/Absent/Late): ")

    cursor.execute("""
        INSERT INTO Attendance (student_id, course_id, date, status)
        VALUES (?, ?, ?, ?)
    """, (student_id, course_id, date, status))

    conn.commit()
    print("Attendance added successfully.")

def show_course_attendance():
    course_name = input("Enter course name: ")
    
    cursor.execute("""
        SELECT 
            s.first_name + ' ' + s.last_name AS Student_Name,
            c.name AS Course_Name,
            a.date AS Attendance_Date,
            a.status AS Attendance_Status
        FROM 
            Attendance a
        INNER JOIN Students s ON a.student_id = s.student_id
        INNER JOIN Courses c ON a.course_id = c.course_id
        WHERE c.name = ?;
    """, (course_name,))
    
    results = cursor.fetchall()
    if results:
        print(f"{'Student Name':<25} {'Course':<25} {'Date':<12} {'Status'}")
        print("-" * 75)
        for row in results:
            print(f"{row[0]:<25} {row[1]:<25} {str(row[2]):<12} {row[3]}")
    else:
        print(f"No attendance records found for course: {course_name}")


def show_student_attendance():
    student_id = input("Enter student ID: ")
    
    cursor.execute("""
        SELECT 
            s.first_name + ' ' + s.last_name AS Student_Name,
            c.name AS Course_Name,
            a.date AS Attendance_Date,
            a.status AS Attendance_Status
        FROM 
            Attendance a
        INNER JOIN Students s ON a.student_id = s.student_id
        INNER JOIN Courses c ON a.course_id = c.course_id
        WHERE s.student_id = ?;
    """, (student_id,))
    
    results = cursor.fetchall()
    if results:
         print(f"{'Student Name':<25} {'Course':<25} {'Date':<12} {'Status'}")
         print("-" * 75)
         for row in results:
            print(f"{row[0]:<25} {row[1]:<25} {str(row[2]):<12} {row[3]}")
    else:
        print(f"No attendance records found for student ID: {student_id}")


def delete_attendance():
    attendance_id = int(input("Enter the attendance ID to delete: "))
    
    cursor.execute("DELETE FROM Attendance WHERE attendance_id = ?", (attendance_id,))
    conn.commit()
    print("Attendance record deleted successfully.")

def update_attendance():
    attendance_id = int(input("Enter the attendance ID to update: "))
    cursor.execute("SELECT * FROM Attendance WHERE attendance_id = ?", (attendance_id,))
    result = cursor.fetchone()

    if result is None:
        print("Attendance ID not found.")
        return
    new_student_id = int(input("New Student ID: "))
    new_course_id = int(input("New Course ID: "))
    new_date = get_valid_date("New Date (YYYY-MM-DD): ")
    new_status = input("New Status (Present/Absent/Late): ")
    
    cursor.execute("""
        UPDATE Attendance
        SET student_id = ?, course_id = ?, date = ?, status = ?
        WHERE attendance_id = ?
    """, (new_student_id, new_course_id, new_date, new_status, attendance_id))
    
    conn.commit()
    print("Attendance record updated successfully.")

def main_menu():
    while True:
        print("\n" + "="*50)
        print("      UNIVERSITY PORTAL SYSTEM - MAIN MENU")
        print("="*50)
        print("1. Department Management")
        print("2. Student Management")
        print("3. Faculty Management")
        print("4. Course Management")
        print("5. Enrollment Management")
        print("6. Grades Management")
        print("7. Attendance Management")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            department_menu()
        elif choice == '2':
            student_menu()
        elif choice == '3':
            faculty_menu()
        elif choice == '4':
            course_menu()
        elif choice == '5':
            enrollment_menu()
        elif choice == '6':
            grades_menu()
        elif choice == '7':
            attendance_menu()
        elif choice == '0':
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Please try again.")

def department_menu():
    while True:
        print("\n--- Department Management ---")
        print("1. Add Department")
        print("2. Update Department")
        print("3. Delete Department")
        print("4. View Departments")
        print("5. Number of students in each Department")
        print("6. Faculty Members in Departments")
        print("0. Back to Main Menu")
        ch = input("Choice: ")
        if ch == '1':
            add_department()
        elif ch == '2':
            update_department()
        elif ch == '3':
            delete_department()
        elif ch == '4':
            display_departments()
            time.sleep(4)
        elif ch == '5':
            stu_in_dep()
            time.sleep(4)
        elif ch == '6':
            faculty_in_department()
            time.sleep(4)
        elif ch == '0':
            break
        else:
            print("Invalid input.")

def student_menu():
    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. View Students")
        print("5. View Past Students")
        print("0. Back to Main Menu")
        ch = input("Choice: ")
        if ch == '1':
            add_student()
        elif ch == '2':
            update_student()
        elif ch == '3':
            delete_student()
        elif ch == '4':
            display_students()
            time.sleep(4)
        elif ch == '5':
            display_deleted_students()
            time.sleep(4)
        elif ch == '0':
            break
        else:
            print("Invalid input.")

def faculty_menu():
    while True:
        print("\n--- Faculty Management ---")
        print("1. Add Faculty")
        print("2. Update Faculty")
        print("3. Delete Faculty")
        print("4. View Faculty")
        print("5. Past Faculty")
        print("0. Back to Main Menu")
        ch = input("Choice: ")
        if ch == '1':
            add_teacher()
        elif ch == '2':
            update_faculty_member()
        elif ch == '3':
            delete_faculty_member()
        elif ch == '4':
            display_teachers()
            time.sleep(4)
        elif ch == '5':
            display_deleted_faculty_members()
            time.sleep(4)
        elif ch == '0':
            break
        else:
            print("Invalid input.")

def course_menu():
    while True:
        print("\n--- Course Management ---")
        print("1. Add Course")
        print("2. Update Course")
        print("3. Delete Course")
        print("4. View Courses")
        print("5. Students enrolled in a course")
        print("0. Back to Main Menu")
        ch = input("Choice: ")
        if ch == '1':
            add_course()
        elif ch == '2':
            update_course()
        elif ch == '3':
            delete_course()
        elif ch == '4':
            display_courses()
            time.sleep(4)
        elif ch == '5':
            students_in_courses()
            time.sleep(4)
        elif ch == '0':
            break
        else:
            print("Invalid input.")

def enrollment_menu():
    while True:
        print("\n--- Enrollment Management ---")
        print("1. Enroll Student")
        print("2. Drop Student")
        print("3. View Enrollments")
        print("0. Back to Main Menu")
        ch = input("Choice: ")
        if ch == '1':
            add_student()
        elif ch == '2':
            delete_student()
        elif ch == '3':
            show_enrollments()
            time.sleep(4)
        elif ch == '0':
            break
        else:
            print("Invalid input.")

def grades_menu():
    while True:
        print("\n--- Grades Management ---")
        print("1. Assign Grade")
        print("2. Update Grade")
        print("3. View Grades")
        print("4. Delete Grades")
        print("0. Back to Main Menu")
        ch = input("Choice: ")
        if ch == '1':
            add_grade()
        elif ch == '2':
            update_grade()
        elif ch == '3':
            show_student_grades()
            time.sleep(4)
        elif ch == '0':
            break
        else:
            print("Invalid input.")

def attendance_menu():
    while True:
        print("\n--- Attendance Management ---")
        print("1. Mark Attendance")
        print("2. Update Attendance")
        print("3. View Attendance of a Student")
        print("4. View Attendance of a Course")
        print("0. Back to Main Menu")
        ch = input("Choice: ")
        if ch == '1':
            add_attendance()
        elif ch == '2':
            update_attendance()
        elif ch == '3':
            show_student_attendance()
            time.sleep(4)
        elif ch == '4':
            show_course_attendance()
            time.sleep(4)
        elif ch == '0':
            break
        else:
            print("Invalid input.")

# Call the main menu to start the system
main_menu()
