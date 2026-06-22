import paypalrestsdk
from decouple import config

paypalrestsdk.configure({
    "mode": config("PAYPAL_MODE"),
    "client_id": config("PAYPAL_CLIENT_ID"),
    "client_secret": config("PAYPAL_CLIENT_SECRET")
})


def create_payment(amount):

    payment = paypalrestsdk.Payment({

        "intent": "sale",

        "payer": {
            "payment_method": "paypal"
        },

        "redirect_urls": {
            "return_url": config("PAYPAL_RETURN_URL"),
            "cancel_url": config("PAYPAL_CANCEL_URL")
        },

        "transactions": [
            {
                "amount": {
                    "total": str(amount),
                    "currency": "USD"
                },

                "description": "Wallet Deposit"
            }
        ]
    })

    if payment.create():
        return payment

    return None