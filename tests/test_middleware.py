import asyncio
import random

import pytest
from sentry_sdk import capture_message
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from sentry_asgi import SentryMiddleware


@pytest.fixture
def app():
    app = Starlette(__name__)

    @app.route("/message")
    def hi(request):
        capture_message("hi", level="error")
        return PlainTextResponse("ok")

    app.add_middleware(SentryMiddleware)

    return app


@pytest.mark.xfail
def test_request_data(sentry_init, app, capture_events):
    sentry_init()
    events = capture_events()

    client = TestClient(app)
    response = client.get("/message?foo=bar")
    assert response.status_code == 200

    event, = events
    assert event["transaction"] == "hi"
    assert event["request"]["env"] == {"REMOTE_ADDR": ""}
    assert set(event["request"]["headers"]) == {
        "accept",
        "accept-encoding",
        "host",
        "user-agent",
    }
    assert event["request"]["query_string"] == "foo=bar"
    assert event["request"]["url"].endswith("/message")
    assert event["request"]["method"] == "GET"

    # Assert that state is not leaked
    events.clear()
    capture_message("foo")
    event, = events

    assert "request" not in event
    assert "transaction" not in event


def test_errors(sentry_init, app, capture_events):
    sentry_init()
    events = capture_events()

    @app.route("/error")
    def myerror(request):
        raise ValueError("oh no")

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/error")
    assert response.status_code == 500

    event, = events
    assert event["transaction"] == "test_middleware.test_errors.<locals>.myerror"
    exception, = event["exception"]["values"]

    assert exception["type"] == "ValueError"
    assert exception["value"] == "oh no"
    assert any(
        frame["filename"].endswith("test_middleware.py")
        for frame in exception["stacktrace"]["frames"]
    )
