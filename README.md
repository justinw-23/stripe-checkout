# Description
This project is a sample one-product online store front that leverages Stripe APIs to process payments by guest users and keep inventory of a product. The server-side is built on top of FastAPI, a web framework for setting up routes, referencing external (Stripe) APIs, and handling database management. This project is set up for SQLite3 and utilizes SQLAlchemy for object-relational mapping to seamlessly integrate database operations with Python programs. The backend leverages a webhook route to listen for Stripe webhook events in order to gather information to update databases accordingly.

## How to run locally

Follow the steps below to run locally.

**1. Clone and configure the sample**

Clone and configure the sample:

```
git clone https://github.com/justinw-23/stripe-checkout.git
```

Navigate into the respository directory

```
cd stripe-checkout
```

Navigate into the server directory
```
cd server
```

Copy the .env.example file into a file named .env in the server directory

```
cp .env.example .env
```

You will need a Stripe account in order to run the demo. Once you set up your account, go to the Stripe [developer dashboard](https://stripe.com/docs/development#api-keys) to find your API keys.

```
STRIPE_PUBLISHABLE_KEY=<replace-with-your-publishable-key>
STRIPE_SECRET_KEY=<replace-with-your-secret-key>
```

The other environment variables are configurable:

`STATIC_DIR` tells the server where the client files are located and does not need to be modified unless you move the server files.

`DOMAIN` is the domain of your website, where Checkout will redirect back to after the customer completes the payment on the Checkout page.

**2. Create a Price**

[![Required](https://img.shields.io/badge/REQUIRED-TRUE-ORANGE.svg)](https://shields.io/)


You can create Products and Prices in the Dashboard or with the API. This sample requires a Price to run. Once you've created a Price, and add its ID to your `.env`.

`PRICE` is the ID of a [Price](https://stripe.com/docs/api/prices/create) for your product. A Price has a unit amount and currency.


You can quickly create a Price with the Stripe CLI like so:

```sh
stripe prices create --unit-amount 500 --currency usd -d "product_data[name]=demo"
```


Which will return the json:

```json
{
  "id": "price_1Hh1ZeCZ6qsJgndJaX9fauRl",
  "object": "price",
  "active": true,
  "billing_scheme": "per_unit",
  "created": 1603841250,
  "currency": "usd",
  "livemode": false,
  "lookup_key": null,
  "metadata": {
  },
  "nickname": null,
  "product": "prod_IHalmba0p05ZKD",
  "recurring": null,
  "tiers_mode": null,
  "transform_quantity": null,
  "type": "one_time",
  "unit_amount": 500,
  "unit_amount_decimal": "500"
}
```

Take the Price ID, in the example case `price_1Hh1ZeCZ6qsJgndJaX9fauRl`, and set the environment variable in `.env`:

```sh
PRICE=price_1Hh1ZeCZ6qsJgndJaX9fauRl
```

**3. Follow the server instructions on how to run**

Follow the instructions in the server folder README on how to run.

**4. Run a webhook locally**

You can use the Stripe CLI to easily spin up a local webhook.

First [install the CLI](https://stripe.com/docs/stripe-cli) and [link your Stripe account](https://stripe.com/docs/stripe-cli#link-account).

```
stripe listen --forward-to localhost:4242/webhook
```

The CLI will print a webhook secret key to the console. Set `STRIPE_WEBHOOK_SECRET` to this value in your `.env` file.

You should see events logged in the console where the CLI is running.
