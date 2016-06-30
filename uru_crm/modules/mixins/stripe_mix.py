import stripe

# from uru_crm.modules.user import User

stripe.api_key = "sk_test_y8bIB8jPLaccPy9a7Tt7ZdAb"


class StripeMixin(object):

    def create_customer(self, card_vals, email=None, plan=None):
        token = stripe.Token.create(card=card_vals).id

        customer = stripe.Customer.create(
            source=token,
            plan=plan,
            email=email
        )

        return customer.id

    def cancel_subscription(self, model, sub_id=None):
        sid = stripe.Customer.retrieve(model.customer_id).subscriptions.data[0].id
        sub = stripe.Subscription.retrieve(sid)
        sub.delete()
