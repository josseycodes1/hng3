
# Country Currency & Exchange API

A RESTful Django API that fetches country data from external APIs, stores it in a database, and provides CRUD operations with currency exchange rates and GDP estimates.

## Features

- Fetch country data from REST Countries API
- Get real-time exchange rates from Exchange Rates API
- Calculate estimated GDP based on population and exchange rates
- CRUD operations for country data
- Filtering and sorting capabilities
- Automatic summary image generation
- Comprehensive error handling

##  Tech Stack

- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL (via Railway)
- **Deployment:** Railway
- **Image Processing:** Pillow (PIL)
- **Environment Management:** python-dotenv

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/countries/refresh` | Fetch and cache countries from external APIs |
| GET | `/countries/` | Get all countries (supports filtering) |
| GET | `/countries/{name}` | Get specific country by name |
| DELETE | `/countries/{name}/delete` | Delete a country record |
| GET | `/countries/status` | Get API status and counts |
| GET | `/countries/image` | Get generated summary image |

### Query Parameters for `/countries/`

- `region` - Filter by region (e.g., `?region=Africa`)
- `currency` - Filter by currency code (e.g., `?currency=USD`)
- `sort` - Sort by GDP (`?sort=gdp_desc` or `?sort=gdp_asc`)

## Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Railway account (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd country-api
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Environment variables
Create a .env file:

env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/countryapi
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=UTC
Run migrations

bash
python manage.py migrate
Start development server

bash
python manage.py runserver
Deployment on Railway
1. Database Setup
Create a new PostgreSQL database on Railway

Copy the database URL from Railway dashboard

2. App Deployment
Connect your GitHub repository to Railway

Add these environment variables in Railway:

env
DEBUG=False
SECRET_KEY=your-strong-secret-key-from-railway
DATABASE_URL=your-railway-postgresql-url
ALLOWED_HOSTS=web-production-c36a5.up.railway.app
CSRF_TRUSTED_ORIGINS=https://web-production-c36a5.up.railway.app
TIME_ZONE=UTC
DRF_PAGE_SIZE=50
3. Build & Deploy
Railway will automatically detect Django and:

Install dependencies from requirements.txt

Run migrations

Collect static files

Start the application

Testing the API
Using Postman or curl
Check status

bash
curl https://web-production-c36a5.up.railway.app/countries/status
Refresh countries data

bash
curl -X POST https://web-production-c36a5.up.railway.app/countries/refresh
Get all countries

bash
curl https://web-production-c36a5.up.railway.app/countries/
Get specific country

bash
curl https://web-production-c36a5.up.railway.app/countries/Nigeria
Get summary image

bash
curl https://web-production-c36a5.up.railway.app/countries/image -o summary.png
Response Formats
Success Responses
Country Object:

json
{
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 25767448125.2,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2024-01-15T10:30:00Z"
}
Error Responses
404 Not Found:

json
{
    "error": "Country not found"
}
400 Validation Error:

json
{
    "error": "Validation failed",
    "details": {
        "currency_code": "is required"
    }
}
500 Internal Server Error:

json
{
    "error": "Internal server error"
}
503 Service Unavailable:

json
{
    "error": "External data source unavailable",
    "details": "Could not fetch data from REST Countries"
}
🔧 Project Structure
text
countryapi/
├── countries/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── exceptions.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── countryapi/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── manage.py
└── README.md
📝 Environment Variables
Variable	Description	Default
DEBUG	Debug mode	False
SECRET_KEY	Django secret key	Required
DATABASE_URL	PostgreSQL connection URL	Required
ALLOWED_HOSTS	Comma-separated allowed hosts	Required
TIME_ZONE	Server timezone	UTC
DRF_PAGE_SIZE	Pagination page size	50
🐛 Troubleshooting
Common Issues
Database connection errors

Verify DATABASE_URL is correct

Check if Railway PostgreSQL is running

External API failures

APIs might be temporarily unavailable

Check Railway logs for details

Image generation issues

Ensure cache directory has write permissions

Run refresh endpoint to regenerate image

Checking Logs on Railway
Go to your Railway project dashboard

Click on "Deployments"

Select your deployment and check "Logs"

📄 License
This project is for educational purposes as part of a backend development assignment.



Live API URL: https://web-production-c36a5.up.railway.app