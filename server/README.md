# Checkout single product

## Requirements

- Python 3
- [Configured .env file](../README.md)

## How to run

1. Confirm `.env` configuration

This sample requires a Price ID in the `PRICE` environment variable.

Open `.env` and confirm `PRICE` is set equal to the ID of a Price from your
Stripe account. It should look something like:

```
PRICE=price_1Hh1ZeCZ6qsJgndJaX9fauRl
```

Note that `price_12345` is a placeholder and the sample will not work with that
price ID. You can [create a price](https://stripe.com/docs/api/prices/create)
from the dashboard or with the Stripe CLI.

2. Create and activate a new virtual environment

**MacOS / Unix**

```
python3 -m venv env
source env/bin/activate
```

**Windows (PowerShell)**

```
python3 -m venv env
.\env\Scripts\activate.bat
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Run fixture

```
python3 fixture.py
```

5. Export and run the application

```
uvicorn server:app --reload --port 4242
```

6. Go to `localhost:4242` to see the demo.

7. [Optional] Use a database visualizer tool such as SQLiteStudio to visualize your SQLite databases.