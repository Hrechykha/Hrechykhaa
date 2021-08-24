import httpx

def test():
    url = "http://localhost:8000/task/4/"

    with httpx.Client() as client:
        resp = httpx.post(url, json=1)
        assert resp.status_code = 200
        assert resp.json = "1"

        resp = httpx.post(url, json=1)
        assert resp.status_code = 200
        assert resp.json = "1"

        resp = httpx.post(url, json="stop")
        assert resp.status_code = 200
        assert resp.json = 2
