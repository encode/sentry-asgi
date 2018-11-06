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


app = ...
app = SentryMiddleware(app, sentry_dsn='...')
```

## Known limitations

The SentryMiddleware will capture and log application exceptions just fine.

Explicitly logging events using the SDK from within views does not appear to work correctly yet.
