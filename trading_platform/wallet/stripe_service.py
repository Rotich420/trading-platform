import stripe
from decouple import config

stripe.api_key = config("STRIPE_SECRET_KEY")


def create_checkout_session(user, amount):

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],

        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Wallet Deposit"
                    },
                    "unit_amount": int(amount * 100)
                },
                "quantity": 1
            }
        ],

        mode="payment",

        success_url=config("STRIPE_SUCCESS_URL"),

        cancel_url=config("STRIPE_CANCEL_URL"),

        metadata={
            "user_id": user.id,
            "amount": str(amount)
        }
    )

    return session