# Fit Control - Multi-Tenant SaaS Fitness Club Management Platform

Production-ready multi-tenant SaaS platform for managing fitness clubs with subscription system, Telegram bot integration, and QR code authentication.

## Tech Stack

- **Backend**: Python Django + Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: HTML + TailwindCSS CDN + Alpine.js
- **Telegram Bot**: aiogram 3.x
- **Platform Language**: Uzbek/Russian

## Features

### Superuser Dashboard
- Manage gyms (CRUD operations)
- Manage subscription plans (monthly, yearly, lifetime)
- Assign subscriptions to gyms
- 14-day free trial system
- Auto-block gyms after subscription expiration
- View gym statistics
- Generate admin login credentials for gyms

### Gym Admin Dashboard
- Manage clients
- Track monthly payments (monitoring only)
- Manage expenses
- View income, expenses, profit statistics
- Subscription status check
- QR code generation for client onboarding

### Subscription System
- Free trial (14 days)
- Monthly / Yearly / Lifetime plans
- Status tracking (trial, active, expired)
- Automatic expiration handling

### Telegram Bot
- Client interaction via QR-based onboarding
- Payment reminders
- Promotions
- Admin quick stats

### QR Code Login
- Unique QR per gym
- Deep linking with Telegram bot

### Landing Page
- Product presentation
- Pricing display
- Free trial registration form
- Backend integration to auto-create gym and trial

## Project Structure

```
fit_control/
├── backend/
│   ├── fit_control/          # Django project settings
│   ├── core/                 # Core models (User, QRCode)
│   ├── gyms/                 # Gym models and views
│   ├── subscriptions/        # Subscription plans
│   ├── clients/              # Client management
│   ├── payments/             # Payment tracking
│   ├── expenses/             # Expense tracking
│   └── requirements.txt
├── frontend/
│   ├── templates/            # HTML templates
│   └── static/               # Static files
├── bot/                      # Telegram bot
└── migrations/               # Database migrations
```

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Telegram Bot Token

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=fit_control
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_BOT_USERNAME=your-bot-username
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

### Frontend Setup

Frontend uses CDN for TailwindCSS and Alpine.js, so no build step is required. Templates are served by Django.

### Telegram Bot Setup

1. Install dependencies:
```bash
cd bot
pip install -r requirements.txt
```

2. Create `.env` file:
```env
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_BOT_USERNAME=your-bot-username
API_BASE_URL=http://localhost:8000
```

3. Run bot:
```bash
python main.py
```

## Usage

### Superuser Dashboard

1. Login at `/admin/` or use API at `/api/auth/login/`
2. Access superuser dashboard
3. Create gyms and assign subscription plans
4. Monitor gym statistics

### Gym Admin Dashboard

1. Login with gym admin credentials
2. Manage clients, payments, and expenses
3. View statistics and subscription status
4. Generate QR codes for client onboarding

### Landing Page

1. Visit landing page
2. View pricing plans
3. Register for free trial
4. Gym and admin account are automatically created

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/me/` - Current user info
- `GET /api/auth/qr-code/` - Get QR code for gym

### Superuser
- `GET /api/superuser/gyms/` - List all gyms
- `POST /api/superuser/gyms/` - Create gym
- `GET /api/superuser/gyms/{id}/` - Get gym details
- `POST /api/superuser/gyms/{id}/assign_subscription/` - Assign subscription
- `POST /api/superuser/gyms/{id}/create_admin/` - Create admin user

### Gym Admin
- `GET /api/gym/my_gym/` - Get current gym
- `GET /api/gym/statistics/` - Get gym statistics
- `GET /api/clients/` - List clients
- `POST /api/clients/` - Create client
- `GET /api/payments/` - List payments
- `POST /api/payments/` - Create payment
- `GET /api/expenses/` - List expenses
- `POST /api/expenses/` - Create expense

### Subscriptions
- `GET /api/subscriptions/plans/` - List subscription plans

## Management Commands

### Check and Block Expired Subscriptions
```bash
python manage.py check_subscriptions
```

This command checks all gyms and automatically blocks those with expired subscriptions.

## Subscription System

- **Trial**: 14 days free trial for new gyms
- **Monthly**: 30 days subscription
- **Yearly**: 365 days subscription
- **Lifetime**: Permanent subscription

Gyms are automatically blocked when their subscription expires. Use the management command to check and block expired gyms.

## Security

- Multi-tenant isolation via middleware
- CSRF protection
- Session-based authentication
- Permission-based access control

## Production Deployment

1. Set `DEBUG=False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Use environment variables for sensitive data
4. Set up PostgreSQL with proper credentials
5. Configure static files serving
6. Set up SSL/HTTPS
7. Configure Telegram bot webhook for production

## License

This project is proprietary software.

## Support

For issues and questions, please contact the development team.
