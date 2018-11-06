import json
import os
import subprocess

import pytest
import sentry_sdk
from sentry_sdk._compat import reraise, string_types
from sentry_sdk.transport import Transport

SEMAPHORE = "./semaphore"

if not os.path.isfile(SEMAPHORE):
    SEMAPHORE = None


@pytest.fixture
def monkeypatch_test_transport(monkeypatch):
    def check_event(event):
        def check_string_keys(map):
            for key, value in map.items():
                assert isinstance(key, string_types)
                if isinstance(value, dict):
                    check_string_keys(value)

        check_string_keys(event)

    def inner(client):
        monkeypatch.setattr(client, "transport", TestTransport(check_event))

    return inner


@pytest.fixture
def sentry_init(monkeypatch_test_transport):
    def inner(*a, **kw):
        hub = sentry_sdk.Hub.current
        client = sentry_sdk.Client(*a, **kw)
        hub.bind_client(client)
        monkeypatch_test_transport(sentry_sdk.Hub.current.client)

    return inner


class TestTransport(Transport):
    def __init__(self, capture_event_callback):
        Transport.__init__(self)
        self.capture_event = capture_event_callback
        self._queue = None


@pytest.fixture
def capture_events(monkeypatch):
    def inner():
        events = []
        test_client = sentry_sdk.Hub.current.client
        old_capture_event = test_client.transport.capture_event

        def append(event):
            events.append(event)
            return old_capture_event(event)

        monkeypatch.setattr(test_client.transport, "capture_event", append)
        return events

    return inner
