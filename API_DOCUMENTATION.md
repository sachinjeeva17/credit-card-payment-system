# Credit Card Payment System — API Documentation

## Base URLs
- Django API: `http://127.0.0.1:8000`
- FastAPI payments: `http://127.0.0.1:8001`

### Authorization
Call Django `/api/auth/login/` with username and password. Copy the returned `access` token into the `Authorization: Bearer <access>` header for protected APIs on both servers. Use the **refresh token** for token refresh and logout; keep both tokens private.

## Authentication — Django
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Obtain access and refresh JWT |
| POST | `/api/auth/refresh/` | Obtain new access JWT |
| POST | `/api/auth/logout/` | Blacklist a refresh JWT |
| GET | `/api/auth/me/` | Current user's profile |




## Card management — Django
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/cards/add/` | Save masked-card metadata |
| GET | `/api/cards/` | List my cards |
| GET | `/api/cards/{card_id}/` | Retrieve one of my cards |
| DELETE | `/api/cards/{card_id}/delete/` | Delete my card if permitted |



Do not submit full card numbers or CVV. A card used in a transaction may be protected against deletion by database foreign-key rules.

## Payment simulation — FastAPI
| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/payments` | Create payment, initial status `PENDING` |
| POST | `/payments/{payment_id}/simulate` | Set `SUCCESS` or `FAILED` |



## Transactions — Django
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/transactions/` | My transaction history |

Optional query parameters: `status=SUCCESS|FAILED|PENDING`, `date=YYYY-MM-DD`, `amount=1500`.

## Administrative APIs — Django
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/daily-summary/` | Selected date / today's payment totals |
| GET | `/api/admin/transactions/export/` | Download CSV |
| GET | `/api/admin/logs/` | Read Django admin audit records |

Admin endpoints require staff permissions (`IsAdminUser`). `daily-summary` supports an optional `date` query parameter. CSV export may also be offered as a Django Admin **action** on selected transactions.

## Example status codes
- `200` successful GET/login/update operation
- `201` resource created
- `204` successfully deleted, no response body
- `400` validation error or invalid status transition
- `401` missing/invalid authentication
- `403` authenticated non-admin accessing restricted action
- `404` inaccessible/missing card or payment

## Testing / evidence
Django coverage as reported: **82%** overall for the selected Django apps. FastAPI payment test coverage is not included in this number.

## Important verification notes
Routes in this document reflect the implementation built in the conversation. If your local code differs, treat your generated Django/FastAPI Swagger schemas as the source of truth and update this file and the Postman collection. Do not publish tokens, real card data, passwords, or personal database dumps.
