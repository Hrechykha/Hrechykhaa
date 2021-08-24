import httpx
import pytest

from asgi import app

@pytest.mark.asyncio
async def test():
    url = "/task/4"

    with httpx.Client() as client:
        resp = client.post(url, json=1)
        assert resp.status_code == 200
        assert resp.json() == "1"

        resp = client.post(url, json=1)
        assert resp.status_code == 200
        assert resp.json() == "1"

        resp = client.post(url, json="stop")
        assert resp.status_code == 200
        assert resp.json() == 2
