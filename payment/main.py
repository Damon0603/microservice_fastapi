from math import prod
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection,HashModel
from starlette.requests import Request
import requests

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],

    allow_methods = ["*"],
    allow_headers = ["*"]
)


# THis should be an different Database
redis = get_redis_connection(
    host ="redis-16934.c300.eu-central-1-1.ec2.cloud.redislabs.com",
    port = 16934,
    password = "b3dvXe5AIRyXQPTwOrxjxJeF0FaFdMot",
    decode_responses = True
)


class Order(HashModel):
    product_id = str
    price = float
    fee: float
    total = float
    quantity = int
    status = str #pending | Completed | refunded

    class Meta:
        database = redis


@app.post("/orders")
async def create(request:Request): # id and quantity
    body = await request.json()
    req = requests.get("http://localhost:8000/products/%s" % body["id"])
    product = req.json()
    order = Order(
        product_id = body["id"],
        price = product["price"],
        fee = product["price"],
        total = 1.2 *product["price"],
        quantity = body["quantity"],
        status = "pending"
    )
    order.save()
    order_completed(order)
    return order


def order_completed(order:Order):
    order.status="completed"

    order.save()



