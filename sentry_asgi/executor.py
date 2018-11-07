import concurrent
import functools

import contextvars


class ContextPreservingExecutor(concurrent.futures.ThreadPoolExecutor):
    def submit(self, func, *args, **kwargs):
        context = contextvars.copy_context()
        child = functools.partial(func, *args, **kwargs)
        return super().submit(context.run, child)
