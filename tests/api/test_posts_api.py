import time, json
import pytest
from jsonschema import validate
from playwright.sync_api import sync_playwright
from utils.schemas import POST_SCHEMA, POST_CREATE_SCHEMA

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def api():
    # Contexto de requests de Playwright (no abre navegador)
    with sync_playwright() as p:
        ctx = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={
                "Accept": "application/json; charset=utf-8",
                "Content-Type": "application/json; charset=utf-8",
            }
        )
        yield ctx
        ctx.dispose()

@pytest.mark.smoke
def test_list_posts_contract(api):
    t0 = time.perf_counter()
    resp = api.get("/posts")
    dt = time.perf_counter() - t0

    assert resp.status == 200
    assert "application/json" in resp.headers["content-type"].lower()
    data = resp.json()
    assert isinstance(data, list) and len(data) > 0

    for item in data[:3]:
        validate(instance=item, schema=POST_SCHEMA)

    assert dt < 2.0, f"Respuesta lenta: {dt:.2f}s"

@pytest.mark.regression
@pytest.mark.parametrize("post_id", [1, 5, 10])
def test_get_post_by_id(api, post_id):
    resp = api.get(f"/posts/{post_id}")
    assert resp.status == 200
    body = resp.json()
    validate(instance=body, schema=POST_SCHEMA)
    assert body["id"] == post_id

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.kike
def test_create_post(api):
    payload = {"title": "mi titulo", "body": "mi contenido", "userId": 1}
    resp = api.post("/posts", data=json.dumps(payload))
    assert resp.status in (200, 201)
    body = resp.json()
    validate(instance=body, schema=POST_CREATE_SCHEMA)
    assert body["title"] == payload["title"]
    assert body["userId"] == payload["userId"]
