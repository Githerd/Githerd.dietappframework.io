# DietApp
DietApp is a Django-based web application designed to help users manage their diet and health goals. It provides features for tracking meals, calculating daily calorie requirements, logging journal entries, and planning weekly meals. It also includes a TDEE (Total Daily Energy Expenditure) calculator and functionality for managing user profiles.
## Features
- **User Management**:
  - User registration and authentication.
  - Profile management with BMI calculation.
  - Password reset and update functionality.
- **Meal Management**:
  - Add, view, update, and delete meals.
  - Track meal macros (calories, carbs, protein, fat).
  - Weekly meal planning.
- **Health Tracking**:
  - TDEE Calculator to estimate daily calorie requirements based on user input.
  - Weekly calorie tracking, including calories burned through exercise.
- **Journal**:
  - Add, view, update, and delete journal entries for personal reflections.
- **Other Features**:
  - Contact and About pages.
  - Admin panel for managing app content.
## Tech Stack
- **Backend**:
  - Python 3.11
  - Django 5.1.4
  - PostgreSQL (or SQLite for development)
- **Frontend**:
  - HTML5, CSS3
  - Bootstrap 5
- **Other Libraries**:
  - `django-crispy-forms`
  - `django-debug-toolbar`
  - `django-redis`
  - `Pillow` (for image handling)
  - `Chart.js` (for visualizing macro percentages)
## Installation
### Prerequisites
- Python 3.11 or higher
- PostgreSQL (or SQLite for development)
- Git
- Pipenv or virtualenv (recommended for dependency management)
### Steps
- Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dietapp.git
   cd dietapp
- Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
- Install dependencies:
pip install -r requirements.txt
- Set up the database:
Update your .env file with your database credentials, or use SQLite for development. Example .env file:
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
Then apply migrations:
python manage.py migrate
- Create a superuser:
python manage.py createsuperuser
- Collect static files:
python manage.py collectstatic
- Run the development server:
python manage.py runserver
The app will be available at http://127.0.0.1:8000.
Deployment
DietApp is designed for deployment on platforms like Render or Heroku. Follow their respective guidelines to deploy your Django app.

## Example Deployment Steps:

- **Install gunicorn and whitenoise for production:**
 pip install gunicorn whitenoise

- **Update settings.py:**
  STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

- **Use environment variables for secrets in production (e.g., SECRET_KEY, DEBUG).**

- **Configure Procfile for Gunicorn:**
  web: gunicorn dietapp.wsgi:application
  
## Usage
	1.	Register as a user.
	2.	Log in and set up your profile.
	3.	Add meals and track their macros.
	4.	Use the TDEE calculator to determine your daily energy needs.
	5.	Plan your weekly meals.
	6.	Log daily reflections in the journal.


Here's a link to the Dietapp Application <https://githerd-dietappframework-io.onrender.com>
