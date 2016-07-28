import stripe
import datetime
import time
import json
import os
from uru_crm.extensions import db


# from uru_crm.modules.user import User

stripe.api_key = 'sk_test_y8bIB8jPLaccPy9a7Tt7ZdAb'


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(time.mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)


def create_customer(card_vals, email=None):
    token = stripe.Token.create(card=card_vals).id

    customer = stripe.Customer.create(
        source=token,
        email=email
    )

    return customer.id


def create_subscription(customer):
    days = abs(datetime.date.today().weekday() - 9)
    start = datetime.date.today() + datetime.timedelta(days=days)
    start = int(time.mktime(start.timetuple()))
    # start = 5
    return stripe.Subscription.create(
        customer=customer.customer_id,
        plan=customer.box_size,
        trial_end=start
    )


def cancel_subscription(customer):
    sid = stripe.Customer.retrieve(customer.customer_id).subscriptions.data[0].id
    sub = stripe.Subscription.retrieve(sid)
    sub.delete()


def update_subscription(model, new_plan=None):
    sid = stripe.Customer.retrieve(model.customer_id).subscriptions.data[0].id
    sub = stripe.Subscription.retrieve(sid)
    sub.plan = new_plan
    print('unix timestamp:::: ')
    print(sub.current_period_end)
    print('unix timestamp:::: ')
    print(type(sub.current_period_end))
    print(sub)
    sub.proration_date = sub.current_period_end
    # sub.status = 'trialing'
    sub.trial_end = sub.current_period_end
    print(sub)
    sub.save()
    print(sub)
    return sub
