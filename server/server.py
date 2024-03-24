#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

import os
from typing import Optional
from fastapi import FastAPI, Form, Header, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import stripe
from database import db_dependency
import models
import logging
from dotenv import load_dotenv, find_dotenv

# Setup Stripe python client library.
load_dotenv(find_dotenv())

# Ensure environment variables are set.
price = os.getenv('PRICE')
if price is None or price == 'price_12345' or price == '':
    print('You must set a Price ID in .env. Please see the README.')
    exit(0)

# For sample support and debugging, not required for production:
stripe.set_app_info(
    'stripe-samples/accept-a-payment/prebuilt-checkout-page',
    version='0.0.1',
    url='https://github.com/stripe-samples')

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = '2020-08-27'

static_dir = str(os.path.abspath(os.path.join(
    __file__, "..", os.getenv("STATIC_DIR"))))

templates = Jinja2Templates(directory=static_dir)

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get('/')
def get_example(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/{cid}/orders')
def get_orders_by_customer_id(cid: int, db: db_dependency, request: Request):
    db_customer = db.query(models.Customer).filter_by(id=cid).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db_orders = db_customer.orders
    return templates.TemplateResponse('orders.html', {'request': request, 'customer': db_customer, 'orders': db_orders})

# Fetch the Checkout Session to display the JSON result on the success page
@app.get('/checkout-session')
def get_checkout_session(
    sessionId : str
):
    id = sessionId
    checkout_session = stripe.checkout.Session.retrieve(id)
    return checkout_session


@app.post('/create-checkout-session')
def create_checkout_session(db: db_dependency, quantity: int = Form(...)):
    domain_url = os.getenv('DOMAIN')
    book = db.query(models.Book).first()
    if book.stock == 0:
        raise HTTPException(status_code=400, detail="Book is out of stock.")
    if quantity > book.stock:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    try:
        # Create new Checkout Session for the order
        # Other optional params include:

        # For full details see https:#stripe.com/docs/api/checkout/sessions/create
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + '/static/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + '/static/canceled.html',
            payment_method_types=(os.getenv('PAYMENT_METHOD_TYPES') or 'card').split(','),
            mode='payment',
            line_items=[{
                'price': os.getenv('PRICE'),
                'quantity': quantity,
            }]
        )
        return RedirectResponse(
            checkout_session.url, 
            status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        raise HTTPException(403, str(e))

@app.post('/webhook')
async def webhook_received(
    db: db_dependency,
    request: Request,
    stripe_signature: Optional[str] = Header(None)
):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = await request.body()
    # request_data = json.loads(request.data)
    logging.basicConfig(level=logging.INFO)
    
    logging.info("************************")
    logging.info("WEBHOOK RECEIVED!")
    logging.info("************************")

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = stripe_signature
        try:
            event = stripe.Webhook.construct_event(
                payload=request_data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)
    logging.info(event_type)
    if event_type == 'checkout.session.completed':
        logging.info('🔔 Payment succeeded!')
        # Note: If you need access to the line items, for instance to
        # automate fullfillment based on the the ID of the Price, you'll
        # need to refetch the Checkout Session here, and expand the line items:
        
        print(data)
        session = stripe.checkout.Session.retrieve(
            data['object']['id'], expand=['line_items'])
        
        
        customer_details = data['object']['customer_details']
        customer_name = customer_details['name']
        print(customer_details)
        line_items = session.line_items
        
        # Update database based on purchased items
        quantity_purchased = None
        for item in line_items:
            quantity_purchased = item['quantity']

            book = db.query(models.Book).first()
            if book:
                book.stock -= quantity_purchased
                book.sold += quantity_purchased
                db.commit()
        
        db_customer = db.query(models.Customer).filter_by(name=customer_name).first()
        if not db_customer:
            db_customer = models.Customer(name=customer_name)
            db.add(db_customer)
            db.commit()
            db.refresh(db_customer)
        db_order = models.Order(customer_id=db_customer.id, book_id=1, quantity=quantity_purchased)
        db.add(db_order)
        db.commit()
        
        
                
        # Read more about expand here: https://stripe.com/docs/expand
    return {'status': 'success'}


# LOG_FILENAME = 'webhook.log'
# logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format='%(asctime)s %(message)s')

# @app.post("/webhook")
# async def webhook_received(request: Request, stripe_signature: str = Header(None)):
#     logging.info("------------------------------------------------------------------------")
#     webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
#     data = await request.body()

#     try:
#         event = stripe.Webhook.construct_event(
#             payload=data,
#             sig_header=stripe_signature,
#             secret=webhook_secret
#         )
#         event_data = event['data']
#     except Exception as e:
#         logging.error("Error in webhook: %s", str(e))
#         return {"error": str(e)}

#     event_type = event['type']
#     logging.info(f"Received event: {event_type}")

#     if event_type == 'checkout.session.completed':
#         logging.info('Checkout session completed')
#     elif event_type == 'invoice.paid':
#         logging.info('Invoice paid')
#     elif event_type == 'invoice.payment_failed':
#         logging.info('Invoice payment failed')
#     else:
#         logging.info(f'Unhandled event: {event_type}')
    
#     return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=4242,
        # ssl_keyfile= Path(__file__).absolute().parents[0] / 'localhost.key',
        # ssl_certfile= Path(__file__).absolute().parents[0] / 'localhost.crt'
    )