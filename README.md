# SCATS Map

In Victoria ...

This app was made to ...

<br>

# REST API

The REST API to the app is described below.

## Users

### User Create

#### Request

```
curl --location --request POST 'http://127.0.0.1:8000/auth/users/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "test@test.com",
    "password": "testpass123",
    "re_password": "testpass123"
}'
```

#### Response

```
{
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "",
    "email": "test@test.com",
    "id": 1
}
```

<br>

### User Activate

#### Request

```
curl --location --request POST 'http://127.0.0.1:8000/auth/users/activation/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "uid": "MTE",
    "token": "ar9fx6-0088631a406fc6eb96d4ac5ec007eaeb"
}'
```

#### Response

```
204 No Content - HTTP
```

<br>

### Create JWT Token

#### Request

```
curl --location --request POST 'http://localhost:8000/auth/jwt/create/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test@test.com",
    "password": "testpass123"
}'
```

#### Response

```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNTQyNjY4NCwianRpIjoiYzc2MzIzYjAzYzM1NGY5NWE1ODliZjY5YzBlNDEzYTYiLCJ1c2VyX2lkIjoxfQ.HjgAD9F7F9IZgOuqMhzkbeYI_XXyO9WMH8_L4jLAEKs",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI2Njg0LCJqdGkiOiI5OTg1NGFhYmMxMTU0ZmU3YTRiZDFmMDY0ZDY4ZTNlZiIsInVzZXJfaWQiOjF9.BSHbHFmGurhEHIYrWfnv5MxKVgV6IV9wbc0Itr8Hdsg"
}
```

<br>

### Refresh JWT Token

#### Request

```
curl --location --request POST 'http://127.0.0.1:8000/auth/jwt/refresh/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNTQyNjY4NCwianRpIjoiYzc2MzIzYjAzYzM1NGY5NWE1ODliZjY5YzBlNDEzYTYiLCJ1c2VyX2lkIjoxfQ.HjgAD9F7F9IZgOuqMhzkbeYI_XXyO9WMH8_L4jLAEKs"
}'
```

#### Response

```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI3MjMxLCJqdGkiOiIyNmZjNDQwYTQxMDU0OGYxODQxYmJmMzYyZjYyOTU4MCIsInVzZXJfaWQiOjF9.ZP5dOICYffTkw46G0S54fgXIdwsPGzrikL_NHeUxP18"
}
```

<br>

### Reset Password

#### Request

```
curl --location --request POST 'http://127.0.0.1:8000/auth/users/reset_password/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test@test.com"
}'
```

#### Response

```
204 No Content - HTTP
```

<br>

### User Detail

#### Request

```
curl --location --request GET 'http://127.0.0.1:8000/users/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI3MjMxLCJqdGkiOiIyNmZjNDQwYTQxMDU0OGYxODQxYmJmMzYyZjYyOTU4MCIsInVzZXJfaWQiOjF9.ZP5dOICYffTkw46G0S54fgXIdwsPGzrikL_NHeUxP18'
```

#### Response

```
{
    "id": 1,
    "email": "test@test.com",
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "",
    "scats_credit": 0,
    "seasonality_credit": 0,
    "subscribed": false,
    "subscription_id": "",
    "free_until": "2021-10-28T13:02:53.116919Z"
}
```

<br>

## SCATS

### Download OpSheet

#### Request

```
curl --location --request GET 'http://127.0.0.1:8000/scats/opsheet-download/100' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI3MjMxLCJqdGkiOiIyNmZjNDQwYTQxMDU0OGYxODQxYmJmMzYyZjYyOTU4MCIsInVzZXJfaWQiOjF9.ZP5dOICYffTkw46G0S54fgXIdwsPGzrikL_NHeUxP18'
```

#### Response

```
{
    "url": "https://scatsmap.s3.amazonaws.com/100.zip?AWSAccessKeyId=AKIAWOG5V5LFV5GOHRBO&Signature=PIlDrRyqWc22aszEAObS6tyA43k%3D&Expires=1635344784"
}
```

<br>

### Extract SCATS data

#### Request

```
curl --location --request GET 'http://localhost:8000/scats/extract-scats-data/?scats_id=100&from=2021-07-01&to=2021-07-03' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI3MjMxLCJqdGkiOiIyNmZjNDQwYTQxMDU0OGYxODQxYmJmMzYyZjYyOTU4MCIsInVzZXJfaWQiOjF9.ZP5dOICYffTkw46G0S54fgXIdwsPGzrikL_NHeUxP18'
```

#### Response

```
[
    {
        "id": 1,
        "NB_SCATS_SITE": 100,
        "QT_INTERVAL_COUNT": "2021-07-01",
        "NB_DETECTOR": 1,
        "V00": 3,
        "V01": 3,
        "V02": 4,
        "V03": 2,
        "V04": 3,
        "V05": 1,
        "V06": 3,
        "V07": 1,
        "V08": 1,
        ...
    },
    {
        "id": 204078,
        "NB_SCATS_SITE": 100,
        "QT_INTERVAL_COUNT": "2021-07-03",
        "NB_DETECTOR": 24,
        "V00": 0,
        "V01": 0,
        "V02": 0,
        "V03": 0,
        "V04": 0,
        "V05": 0,
        ...
    },
    ...
]
```

<br>

### Seasonality analysis

#### Request

```
curl --location --request GET 'http://localhost:8000/scats/seasonality-analysis/?scats_id=100&from=2021-07-01&to=2021-07-03&detectors=1' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI3MjMxLCJqdGkiOiIyNmZjNDQwYTQxMDU0OGYxODQxYmJmMzYyZjYyOTU4MCIsInVzZXJfaWQiOjF9.ZP5dOICYffTkw46G0S54fgXIdwsPGzrikL_NHeUxP18'
```

#### Response

```
{
    "schema": {
        "fields": [
            ...
        ]
    },
    "data": [
        {
            "QT_INTERVAL_COUNT": "2021-07-01T00:00:00.000Z",
            "V00": 3.0,
            "V01": 3.0,
            "V02": 4.0,
            "V03": 2.0,
            "V04": 3.0,
            ...
        },
        {
            "QT_INTERVAL_COUNT": "2021-07-02T00:00:00.000Z",
            "V00": 1.0,
            "V01": 5.0,
            "V02": 2.0,
            "V03": 1.0,
            "V04": 3.0,
            ...
        },
        {
            "QT_INTERVAL_COUNT": "2021-07-03T00:00:00.000Z",
            "V00": 2.0,
            "V01": 6.0,
            "V02": 2.0,
            "V03": 8.0,
            "V04": 3.0,
            ...
        }
    ]
}

```

<br>

## Payments

### Create checkout session

#### Request

```
curl --location --request POST 'http://localhost:8000/payments/create-checkout-session/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI4NzU3LCJqdGkiOiI4YmNjYzI3NmUwN2E0NDgxYmIzMjhiNDZhYjBhYWM4MSIsInVzZXJfaWQiOjJ9.ilmzsdaCtnU6h5Y5b3dyAluuwUr6SVVzTvLoru6SNqU' \
--header 'Content-Type: application/json' \
--data-raw '{
    "orders": [
        {
            "price_id": "price_1JOIC1CJUgzn1x20mQu8fGmH",
            "quantity": 5
        },
        {
            "price_id": "price_1JOICJCJUgzn1x207berWDaX",
            "quantity": 10
        }
    ]
}

'

```

#### Response

```
{
    "checkout_url": "https://checkout.stripe.com/pay/cs_test_b1RKyxPoqZCPjdqYN5TyGb3qaI97IfTTJUK89235H1QpZHJbtY2Fr5onWF#fidkdWxOYHwnPyd1blpxYHZxWjA0TGJMSEtGT1Bif2s0fTc1YXNsVWZ%2FY3Vja2Bpa09hYkNRd1dSfU1uYzBnb2wydXx2YE1dT1IyVzxCRjU9ZDNSRG5NPX9wcXZUdFFSVnVQUVVsR0FVTE5qNTVrRzxqU0JqNCcpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPydocGlxbFpscWBoJyknYGtkZ2lgVWlkZmBtamlhYHd2Jz9xd3BgeCUl"
}

```

<br>

### Create checkout session - Monthly Subscription

#### Request

```
curl --location --request POST 'http://localhost:8000/payments/create-checkout-session/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI5MzQ0LCJqdGkiOiJkNzM5ZDBhZTg4YWM0MzY1ODI5ZWIzNTJkNGU4OTUxNCIsInVzZXJfaWQiOjN9.iCrDNL39gmxRQ8AYFFWhisCpdRAJAumJpnYetMElyhw' \
--header 'Content-Type: application/json' \
--data-raw '{
    "subscription": true
}
'

```

#### Response

```
{
    "checkout_url": "https://checkout.stripe.com/pay/cs_test_a1UOIBEwRlSRtquFltkphoPEqyKyYxm9wf8qd5HHzWEjFK4ATTb5fPU0ap#fidkdWxOYHwnPyd1blpxYHZxWjA0TGJMSEtGT1Bif2s0fTc1YXNsVWZ%2FY3Vja2Bpa09hYkNRd1dSfU1uYzBnb2wydXx2YE1dT1IyVzxCRjU9ZDNSRG5NPX9wcXZUdFFSVnVQUVVsR0FVTE5qNTVrRzxqU0JqNCcpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
}

```

<br>

### Get subscription information

#### Request

```
curl --location --request GET 'hhttp://localhost:8000/payments/get-subscription-info/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI4NzU3LCJqdGkiOiI4YmNjYzI3NmUwN2E0NDgxYmIzMjhiNDZhYjBhYWM4MSIsInVzZXJfaWQiOjJ9.ilmzsdaCtnU6h5Y5b3dyAluuwUr6SVVzTvLoru6SNqU'

```

#### Response

```
{
    "id": "sub_K2NcJPTNJPm1sM",
    "created": "2021-08-14T19:09:04+10:00",
    "cancel_at": null,
    "cancel_at_period_end": false,
    "canceled_at": null,
    "current_period_start": "2021-10-27T20:09:04+11:00",
    "current_period_end": "2021-10-28T20:09:04+11:00",
    "ended_at": null,
    "status": "active",
    "plan": {
        "amount_decimal": "20000.000000000000",
        "currency": "aud",
        "interval": "day",
        "interval_count": 1,
        "product": {
            "name": "Subscription"
        }
    }
}

```

<br>

### Cancel subscription

#### Request

```
curl --location --request POST 'http://localhost:8000/payments/cancel-subscription/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI4NzU3LCJqdGkiOiI4YmNjYzI3NmUwN2E0NDgxYmIzMjhiNDZhYjBhYWM4MSIsInVzZXJfaWQiOjJ9.ilmzsdaCtnU6h5Y5b3dyAluuwUr6SVVzTvLoru6SNqU'

```

#### Response

```
{
    "message": "Your subscription will be cancelled at the end of the current billing period."
}

```

<br>

### Reactivate cancelled subscription

#### Request

```
curl --location --request POST 'http://localhost:8000/payments/reactivate-cancelled-subscription/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM1NDI4NzU3LCJqdGkiOiI4YmNjYzI3NmUwN2E0NDgxYmIzMjhiNDZhYjBhYWM4MSIsInVzZXJfaWQiOjJ9.ilmzsdaCtnU6h5Y5b3dyAluuwUr6SVVzTvLoru6SNqU'
```

#### Response

```
{
    "message": "Your subscription is now successfully reactivated."
}
```
