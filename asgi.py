import json


async def application(scope, receive, send) -> None:
    if scope["type"] != "http":
        return

    path = scope["path"]

    await send(
        {
            "headers": [
                [b"content-type", b"application/json"],
            ],
            "status": 200,
            "type": "http.response.start",
        }
    )

    payload = {
        "hello": "world",
        "path": path,
    }

    body = json.dumps(payload).encode()

    await send(
        {
            "body": body,
            "type": "http.response.body",
        }
    )

