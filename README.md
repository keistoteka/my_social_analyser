# Social Media Footprint Analysis System

## Project Structure

The project is organized into the following main parts:

### 1. Models (Data Models)
- `models/user.py` - User and social media profile models
  - `User` - user data model
  - `SocialProfile` - social media profile model

### 2. Forms (Form Classes)
- `forms/auth.py` - Authentication forms
  - `LoginForm` - login form
  - `RegistrationForm` - registration form
  - `ChangePasswordForm` - password change form

### 3. Services (Business Logic)
- `services/auth_service.py` - Authentication logic
  - User registration
  - Login verification
  - Password change
  - Account deletion

### 4. Routes (Routes)
- `routes/auth.py` - Authentication routes
  - Registration
  - Login
  - Logout
  - Profile management
- `routes/main.py` - Main routes
  - Home page
  - Dashboard
  - Analysis page

### 5. Utils (Utility Functions)
- `utils/__init__.py` - Package initialization

### Main Files
- `app.py` - Application configuration and initialization
- `run.py` - Application entry point

## Functionality

1. User Management:
   - Registration
   - Login
   - Password change
   - Account deletion

2. Social Media Profile Management:
   - Profile addition
   - Profile viewing
   - Profile analysis

3. Data Analysis:
   - Social media footprint analysis
   - Data visualization

## Technologies

- Backend: Python, Flask
- Database: SQLite
- Frontend: HTML, CSS (Tailwind CSS), JavaScript
- Authentication: Flask-Login
- Form Management: Flask-WTF

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit the .env file
```

3. Run the application:
```bash
python run.py
```

## Security

- Passwords are stored hashed
- Session management
- CSRF protection
- Login requirements for protected pages

Trumpa instrukcija, ką turi padaryti TU:
Gauti Ayrshare/Hootsuite API raktus (užsiregistruoti ir gauti API key).
Įrašyti šiuos duomenis į .env failą.
(Jei reikia) Užregistruoti savo programą Pushshift API (arba naudoti viešą endpointą).