# Credit Card Payment System

A learning/demo credit-card payment system using **Django REST Framework**, **FastAPI**, and **MySQL**. Payments are **simulated**; this application does not charge real cards.

## Modules
- Django: account registration, JWT login/refresh/logout, profile
- Django: card creation, list, lookup, deletion (where allowed)
- FastAPI: create a pending payment, simulate SUCCESS/FAILED
- Django: transaction history and optional status/date/amount filters
- Admin: users, cards, transactions, daily summary, CSV export, admin logs

## Project structure
```text
credit_card_payment/
  accounts/
  cards/
  transactions/
  payment_service/main.py
  config/
  manage.py
  .env                 # create locally; NEVER commit
  requirements.txt

```

## Local setup (Windows PowerShell)
1. Open project folder in VS Code.
2. Create and activate a virtual environment:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
3. In MySQL, create a development database and database user, then configure `.env` with the same keys as `config/settings.py` expects. Example:
```env
DB_NAME=credit_card_payment_v2
DB_USER=card_app
DB_PASSWORD=REPLACE_WITH_LOCAL_PASSWORD
DB_HOST=localhost
DB_PORT=3306
```
4. Ensure `SECRET_KEY`, `DEBUG`, and database credentials are configured safely for your environment. Never commit secrets.
5. Apply migrations and start Django:
```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
6. In a **second terminal** (with the virtual environment active), start FastAPI:
```powershell
python -m uvicorn payment_service.main:app --reload --port 8001
```

## Documentation and admin URLs
- Django Swagger: http://127.0.0.1:8000/api/docs/
- Django OpenAPI schema: http://127.0.0.1:8000/api/schema/
- FastAPI Swagger: http://127.0.0.1:8001/docs
- FastAPI OpenAPI: http://127.0.0.1:8001/openapi.json
- Django Admin: http://127.0.0.1:8000/admin/

## Basic test flow
Register -> Login -> copy the **access** JWT -> Add card -> Create PENDING payment in FastAPI -> Simulate SUCCESS/FAILED -> View transaction history in Django.

## API documentation
See `API_DOCUMENTATION.md` and import `Credit_Card_Payment.postman_collection.json` into Postman. Use **access** token for protected endpoints; logout consumes **refresh** token.

## Database tables
- `auth_user`: Django built-in account, registration timestamp (`date_joined`) and last login (`last_login`)
- `cards_card`: owned masked card details (brand, last4, expiry)
- `transactions_transaction`: reference, user, card, amount, currency, status, failure reason, created time
- `django_admin_log`: Django Admin changes and custom actions that explicitly log
- JWT blacklist tables: outstanding/blacklisted refresh tokens

## Testing
Current reported coverage for `accounts`, `cards`, and `transactions` Django modules: **82% (371 statements, 65 missed)**. This does **not** measure FastAPI coverage.
```powershell
python manage.py test accounts cards transactions
coverage run --source=accounts,cards,transactions manage.py test accounts cards transactions
coverage report -m
coverage html
```
Include screenshots of the actual passing test run and coverage output. The seven-test run was reported by the developer, but a full passing summary (`OK`) should be confirmed.

## Security and limitations
- Do not store full card number or CVV; keep only last four digits and masked rendering.
- Card endpoints must filter on the authenticated user.
- Payment processing is simulated; not PCI-certified or suitable for real funds.
- Django `LogEntry` only records admin-site operations and explicitly instrumented actions, not every JWT/API event.
- Verify token permissions, migration behavior, card deletion with transactions, payment status concurrency, and complete FastAPI test coverage before deployment.

## Screenshots to collect
1. Django Swagger list and JWT authorization
2. FastAPI Swagger payment endpoints
3. Successful and failed payment responses (hide tokens)
4. Django Admin users with date joined and last login
5. Saved card list and transactions list
6. Daily summary and exported CSV
7. Test coverage report
8. MySQL schema in Workbench
9. Postman collection
10. GitHub repository with commit history

## GitHub submission
```powershell
git init
git add .
git commit -m "docs: add API documentation and Postman collection"
git branch -M main
git remote add origin https://github.com/sachinjeeva17/credit-card-payment-system.git
git push -u origin main
```

