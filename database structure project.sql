create database university_portal;

use university_portal;

CREATE TABLE Departments (
    department_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    building NVARCHAR(100)
);

CREATE TABLE Students (
    student_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    phone NVARCHAR(20),
    date_of_birth DATE,
    department_id INT FOREIGN KEY REFERENCES Departments(department_id),
    enrollment_date DATE
);

CREATE TABLE FacultyMember (
    faculty_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    department_id INT FOREIGN KEY REFERENCES Departments(department_id),
    hire_date DATE
);

CREATE TABLE Courses (
    course_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    credits INT CHECK (credits > 0),
    department_id INT FOREIGN KEY REFERENCES Departments(department_id),
    faculty_id INT FOREIGN KEY REFERENCES FacultyMember(faculty_id)
);

CREATE TABLE Enrollments (
    enrollment_id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT FOREIGN KEY REFERENCES Students(student_id),
    course_id INT FOREIGN KEY REFERENCES Courses(course_id),
    enrolled_on DATE,
    semester NVARCHAR(20)
);

CREATE TABLE Grades (
    grade_id INT IDENTITY(1,1) PRIMARY KEY,
    enrollment_id INT FOREIGN KEY REFERENCES Enrollments(enrollment_id),
	term NVARCHAR(15),
    grade CHAR(2),
    remarks NVARCHAR(255)
);

CREATE TABLE Attendance (
    attendance_id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT FOREIGN KEY REFERENCES Students(student_id),
    course_id INT FOREIGN KEY REFERENCES Courses(course_id),
    date DATE,
    status NVARCHAR(10) CHECK (status IN ('Present', 'Absent', 'Late'))
);

create table Deleted_students(
    student_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    phone NVARCHAR(20),
    date_of_birth DATE,
    department_id INT FOREIGN KEY REFERENCES Departments(department_id),
    enrollment_date DATE
);

CREATE TRIGGER s1
ON Students
AFTER DELETE
AS
BEGIN
    INSERT INTO Deleted_students (student_id, first_name, last_name, email, phone, date_of_birth, department_id, enrollment_date)
    SELECT student_id, first_name, last_name, email, phone, date_of_birth, department_id, enrollment_date
    FROM deleted;
END;

CREATE TABLE Deleted_faculty_members (
    faculty_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    department_id INT FOREIGN KEY REFERENCES Departments(department_id),
    hire_date DATE
);

CREATE TRIGGER f1
ON FacultyMember
AFTER DELETE
AS
BEGIN
    INSERT INTO Deleted_faculty_members (faculty_id, name, email, department_id, hire_date)
    SELECT faculty_id, name, email, department_id, hire_date
    FROM deleted;
END;

CREATE PROCEDURE students_in_courses
@course_name varchar(100)
AS BEGIN
SELECT s.student_id,s.first_name + ' ' + s.last_name AS Student_Name,
c.name AS Course_Name
FROM Enrollments e
INNER JOIN Students s ON e.student_id = s.student_id
INNER JOIN Courses c ON e.course_id = c.course_id
WHERE LOWER(c.name) = LOWER(@course_name);
END;


 