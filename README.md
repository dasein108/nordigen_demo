# Nordigen demo app

Features:
 - User can connect multiple bank accounts
 - User can see bank accounts and it balances/details
 - User can see all the latest transactions sorted by date and all transactions for particular bank

 Brief:
 - Frontend: React, React-Router, React-Query, Antd Components
 - Backend: Django
 - Due time restrictions:
	 - Auth hardcoded
	 - No tests 
	 - No celery(naked async + caching)
	 - No TypeScript

## Start
-	Launch `docker-compose up`

## Develop 

### Backend
- `cd backend`
 - Fill `.env` file 
 - Install requrements
	 - `python3 -m venv .venv`  
	 -  `.venv/bin/activate`
	- `pip install -Ur requirements.txt`
- run `python manage.py runserver 0.0.0.0:8000`

### Frontend
- `cd frontend`
- `yarn install`
- `yarn start`

## Deploy

 - Tiny example of deploy script for Gitlab CI is attached  `.gitlab-ci.yml`
