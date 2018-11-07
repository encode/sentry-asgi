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
from sentry_asgi.executor import ContextPreservingExecutor  # Python 3.7+

sentry_sdk.init(dsn=...)

app = Starlette()

@app.route("/")
def homepage(request):
    raise ValueError("nope")

@app.on_event("startup")
async def setup_executor():
    executor = ContextPreservingExecutor()
    loop = asyncio.get_event_loop()
    loop.set_default_executor(executor)

app.add_middleware(SentryMiddleware)
```

## Notes

### ThreadPools and execution context

The Sentry SDK requires Python 3.7's `contextvars` support in order to properly
tie messages and logging back to the request context that is added SentryMiddleware.

It is recommended that you install the `ContextPreservingExecutor` as the default
executor, to ensure that Sentry is able to correctly tie related logging, messages,
and breadcrumbs to the middleware request/response context.

Here's an example of how you would do that with Starlette.

```python
from sentry_asgi.executor import ContextPreservingExecutor

...

@app.on_event("startup")
def setup_default_executor():
    executor = ContextPreservingExecutor()
    loop = asyncio.get_event_loop()
    loop.set_default_executor(executor)
```

Other ASGI frameworks should also typically include a "startup" hook,
which is where you'll want to place your executor setup code.

On 3.6 the SentryMiddleware will capture and log application exceptions just fine,
but will not properly tie in logging, messages, or breadcrumbs for any code that
runs within a thread pool executor. (Typically ASGI frameworks will run any regular sync views
within an executor).

For further context [see here](https://github.com/getsentry/sentry-python/issues/162#issuecomment-436257011).

It is possible that Python 3.8 will include support for retaining the correct context
without having to setup a custom executor class.

### Endpoint information

It is recommended that frameworks populate an "endpoint" key in the ASGI scope,
to indicate which view function or class should be logged by the middleware.
