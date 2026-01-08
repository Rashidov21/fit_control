# Setup Guide

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your database and Telegram bot credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# (Optional) Create sample data
python manage.py create_sample_data

# Run server
python manage.py runserver
```

### 2. Frontend Setup

Frontend uses CDN for TailwindCSS and Alpine.js, so no build step is required. Templates are served by Django.

Access the application at:
- Landing page: http://localhost:8000/
- Login: http://localhost:8000/login/
- Superuser dashboard: http://localhost:8000/superuser/
- Gym admin dashboard: http://localhost:8000/gym-admin/

### 3. Telegram Bot Setup

```bash
cd bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your Telegram bot token and API URL

# Run bot
python main.py
```

## Environment Variables

### Backend (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=fit_control
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_BOT_USERNAME=your-bot-username

CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### Bot (.env)

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_BOT_USERNAME=your-bot-username
API_BASE_URL=http://localhost:8000
```

## Database Setup

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE fit_control;
```

3. Update .env with your PostgreSQL credentials
4. Run migrations:
```bash
python manage.py migrate
```

## Creating Telegram Bot

1. Open Telegram and search for @BotFather
2. Send `/newbot` command
3. Follow instructions to create bot
4. Copy the bot token to your .env file
5. Get your bot username and add it to .env

## Testing

### Test Superuser Dashboard

1. Create superuser: `python manage.py createsuperuser`
2. Login at http://localhost:8000/login/
3. Access superuser dashboard

### Test Gym Registration

1. Visit landing page: http://localhost:8000/
2. Fill registration form
3. Gym and admin user will be created automatically
4. 14-day trial will start

### Test Gym Admin Dashboard

1. Login with gym admin credentials
2. Access gym admin dashboard
3. Manage clients, payments, expenses

## Scheduled Tasks

For production, set up a cron job or scheduled task to run:

```bash
python manage.py check_subscriptions
```

This will automatically block gyms with expired subscriptions. Run it daily.

## Production Deployment

1. Set `DEBUG=False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Set up PostgreSQL with proper credentials
4. Configure static files serving (e.g., with nginx)
5. Set up SSL/HTTPS
6. Configure Telegram bot webhook for production
7. Set up scheduled task for subscription checking
