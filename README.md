# sentry-asgi

<a href="https://travis-ci.org/encode/sentry-asgi">
    <img src="https://travis-ci.org/encode/sentry-asgi.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/encode/sentry-asgi">
    <img src="https://codecov.io/gh/encode/sentry-asgi/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/sentry-asgi/">
    <img src="https://badge.fury.io/py/sentry-asgi.svg" alt="Package version">
</a>

Sentry integration for ASGI frameworks.

Installation:

```shell
pip install sentry-asgi
```

Usage:

```python
from sentry_asgi import SentryMiddleware
import sentry_sdk


sentry_sdk.init(dsn=...)

app = ...
app = SentryMiddleware(app)
```

Here's a more complete example, using Starlette:

```python
import sentry_sdk
from sentry_asgi import SentryMiddleware

sentry_sdk.init(dsn=...)

app = Starlette()

@app.route("/")
def homepage(request):
    raise ValueError("nope")

app.add_middleware(SentryMiddleware)
```

## Notes

### Python version support

The Sentry SDK requires Python 3.7's `contextvars` support in order to properly
tie messages and logging back to the request context that is added SentryMiddleware.

On 3.6 and below the SentryMiddleware will capture and log application exceptions just fine,
but will not properly tie in logging, messages, or breadcrumbs for any code that
runs within a threadpool executor or subtask.

ASGI frameworks should ensure that any thread pool executors [preserve the `contextvar` context](https://github.com/django/asgiref/issues/71).

### Endpoint information

It is recommended that frameworks populate an "endpoint" key in the ASGI scope,
to indicate which view function or class should be logged by the middleware.
