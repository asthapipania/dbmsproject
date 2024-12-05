from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Set up database URI (use SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    student_class = db.Column(db.String(50), nullable=False)

# Manually create tables (Ensure this is done before the app starts)
with app.app_context():
    db.create_all()

# Route for the home page, to display all students
@app.route('/')
def index():
    students = Student.query.all()  # Fetch all students from database
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        student_class = request.form['class']
        new_student = Student(name=name, age=age, student_class=student_class)

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect('/')  # After adding a student, redirect to the home page
        except Exception as e:
            return f'There was an issue adding the student: {e}'
    
    return render_template('add.html')  # Return the form when GET request is made

# Route to delete a student by ID
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the student.'

# Route to display the dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    students = Student.query.all()

    # Check if all students have complete details
    for student in students:
        if not student.name or not student.age or not student.student_class:
            return "Please complete all student details before accessing the dashboard."

    return render_template('dashboard.html')

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
