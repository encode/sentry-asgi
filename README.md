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

## Notes

The SentryMiddleware will capture and log application exceptions just fine.

Explicitly logging events using the SDK from within views [does not currently appear to work correctly](https://github.com/getsentry/sentry-python/issues/162#issuecomment-436257011).

It is recommended that frameworks populate an "endpoint" key in the ASGI scope, to indicate which view function or class should be logged by the middleware.
