from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(50), nullable=True)
    reg_no = db.Column(db.String(50), nullable=True, unique=True)
    department = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)


    @app.route("/student", methods=["POST"])
    def create_student():
        data = request.get_json(silent=True) or {}


        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        reg_no = data.get("reg_no")
        department = data.get("department")
        address = data.get("address")

        #if not first_name or not email or not password or not reg_no or not department or not address:
            #return jsonify({"error": "Missing required fields"}), 400

        if not all([first_name, email, password, reg_no, department, address]):
            return jsonify({"error": "Missing required fields"}), 400

        if Student.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400

        student = Student(first_name=first_name, 
                          last_name=last_name, 
                          email=email, 
                          password=password, 
                          reg_no=reg_no, 
                          department=department, 
                          address=address)
        try:
            db.session.add(student)
            db.session.commit()

            return jsonify({
                "message":"Student successfully registered!",
                "student": student.to_response()
            })

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating student: {e}")

            return jsonify({"error": "Unable to create student"}), 500


    @app.route("/students", methods=["GET"])
    def get_students():
        students = Student.query.order_by(Student.id).all()
        return jsonify([student.to_response() for student in students])

    @app.route("/student/<string:reg_no>", methods=["GET"])
    def get_student(reg_no):
        student = Student.query.filter_by(reg_no=reg_no).first()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student.to_response())

    @app.route("/student/<int:id>", methods=["PUT"])
    def update_student(id):
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        data = request.get_json(silent=True) or {}
        student.first_name = data.get("first_name", student.first_name)
        student.last_name = data.get("last_name", student.last_name)
        student.email = data.get("email", student.email)
        student.password = data.get("password", student.password)
        student.reg_no = data.get("reg_no", student.reg_no)
        student.department = data.get("department", student.department)
        student.address = data.get("address", student.address)

        try:
            db.session.commit()
            return jsonify({
                "message": "Student updated successfully!",
                "student": student.to_response()
            })
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating student: {e}")
            return jsonify({"error": "Unable to update student"}), 500

    @app.route("/student/<int:id>", methods=["DELETE"])
    def delete_student(id):
        
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404
#.gitignore
#.env
        try:
            db.session.delete(student)
            db.session.commit()
            return jsonify({"message": "Student deleted successfully!"})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting student: {e}")
            return jsonify({"error": "Unable to delete student"}), 500

# Demo function
    def demo():
        pass

    def to_response(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "reg_no": self.reg_no,
            "department": self.department,
            "address": self.address
        }
    
#Mysql Install, MySQL server, Workbench
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)