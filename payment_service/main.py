import os
import django

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from decimal import Decimal

# Load Django settings and models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from cards.models import Card
from transactions.models import Transaction


app = FastAPI(title="Credit Card Payment API")
security = HTTPBearer()


# Request schema
class PaymentRequest(BaseModel):
    card_id: int
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class PaymentStatusRequest(BaseModel):
    status: str
    failure_reason: str = ""


# Verify Django JWT access token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = AccessToken(credentials.credentials)
        user_id = token["user_id"]

        user = get_user_model().objects.get(
            id=user_id,
            is_active=True
        )

        return user

    except (TokenError, KeyError, get_user_model().DoesNotExist):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
def payment_response(payment):

    card = payment.card

    return {
        "payment_id": payment.id,
        "reference": payment.reference,

        "card_id": card.id,
        "cardholder_name": card.cardholder_name,
        "brand": card.brand,
       

        "masked_number": f"**** **** **** {card.last4}",
       
        "amount": str(payment.amount),
        "currency": payment.currency,

        "status": payment.status,
        "failure_reason": payment.failure_reason,

        "created_at": payment.created_at.isoformat()
    }

@app.get("/health", tags=["health"])
def health():
    return {"message": "Payment service running"}


@app.post("/payments", status_code=201, tags=["payments"])
def create_payment(
    data: PaymentRequest,
    user=Depends(get_current_user)
):

    card = Card.objects.filter(
        id=data.card_id,
        user=user
    ).first()

    if card is None:
        raise HTTPException(
            status_code=404,
            detail="Card not found"
        )

    payment = Transaction.objects.create(
        user=user,
        card=card,
        amount=data.amount,
        currency="INR",
        status="PENDING"
    )

    return payment_response(payment)

@app.post("/payments/{payment_id}/simulate", tags=["payments"])
def simulate_payment(
    payment_id: int,
    data: PaymentStatusRequest,
    user=Depends(get_current_user)
):

    payment = Transaction.objects.select_related("card").filter(
        id=payment_id,
        user=user
    ).first()

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    if payment.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Payment already processed"
        )

    new_status = data.status.upper()

    if new_status not in ["SUCCESS", "FAILED"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment status"
        )

    payment.status = new_status

    if new_status == "FAILED":
        payment.failure_reason = (
            data.failure_reason or "Payment declined"
        )
    else:
        payment.failure_reason = ""

    payment.save()

    return payment_response(payment)