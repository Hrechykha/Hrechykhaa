import os
from collections import defaultdict

from fastapi import Body
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

numbers = defaultdict(list)

def gen_random_name():
    return os.urandom(16).hex()

def get_user(request: Request):
    return request.cookies.get("user")

@app.post("/task/4")
def handler(
        request: Request,
        response: Response,
        data: str = Body(...),
):
    user = get_user(request) or gen_random_name()
    response.set_cookie("user", user)

    if data == "stop":
        return sum(numbers[user])
    else:
        assert data.isdigit()
        numbers[user].append(int(data))
        return numbers[user]