from app import create_app, db
from models.admin import Admin
from werkzeug.security import generate_password_hash

def create_initial_admin():
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        if Admin.query.filter_by(username='admin').first():
            print('Admin user already exists!')
            return

        # Create initial admin user
        admin = Admin(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            is_super_admin=True
        )

        # Add to database
        db.session.add(admin)
        db.session.commit()
        print('Initial admin user created successfully!')
        print('Username: admin')
        print('Password: admin123')
        print('Please change these credentials after first login!')

if __name__ == '__main__':
    create_initial_admin() 