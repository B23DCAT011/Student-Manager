from flask import Flask, blueprints
from app.controllers.auth_controller import auth_bp
from app.controllers.student_controller import student_bp
from app.controllers.teacher_controller import teacher_bp
from app.controllers.academic_controller import academic_bp
from app.controllers.home_controller import home_bp
from app.controllers.grades_controller import grades_bp
from app.controllers.chatbot_controller import chatbot_bp
from app.controllers.email_controller import email_bp
from core.database import init_app, create_tables

app = Flask(__name__, template_folder='app/templates')
app.config.from_object('core.config.Config')

# Initialize database
init_app(app)

# Create tables
# create_tables(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp,)
app.register_blueprint(teacher_bp, )
app.register_blueprint(academic_bp, )
app.register_blueprint(home_bp)
app.register_blueprint(grades_bp, url_prefix='/grades')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
app.register_blueprint(email_bp, url_prefix='/email')

if __name__ == '__main__':
    app.run(debug=True)