# Spend_Smart Django Project

This project is now structured for Django and ready for deployment on Vercel.

## How to deploy on Vercel

1. Make sure your environment variables (like SECRET_KEY) are set in Vercel dashboard.
2. Push your code to GitHub and connect the repo to Vercel.
3. Vercel will auto-detect the Python project and install dependencies from requirements.txt.
4. Static files are handled via WhiteNoise.

## Project Structure
- spendsmart/ : Django project root
- app/ : Main Django app
- static/ : Static files
- templates/ : HTML templates

## Local Development
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
