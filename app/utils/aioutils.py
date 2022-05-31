import asyncio
import concurrent.futures
from functools import partial
from typing import Any, Callable, Coroutine, List, Optional


def run_in_executor(
    func: Callable,
    *args,
    executor: Optional[concurrent.futures.Executor] = None,
    loop: Optional[asyncio.AbstractEventLoop] = None
) -> Coroutine:
    loop = loop or asyncio.get_event_loop()
    return loop.run_in_executor(executor, func, *args)


def gather_in_executor(
    func: Callable,
    items: List,
    expand: bool = False,
    executor: Optional[concurrent.futures.Executor] = None,
    loop: Optional[asyncio.AbstractEventLoop] = None
) -> Coroutine:
    loop = loop or asyncio.get_event_loop()
    _run_in_executor = partial(run_in_executor, executor=executor, loop=loop)
    return asyncio.gather(*[_run_in_executor(func, *(item if expand else (item,))) for item in items])


def gather(coroutine: Coroutine, items: List, expand: bool = False) -> Coroutine:
    return asyncio.gather(*[coroutine(*(item if expand else (item,))) for item in items])


def create_task(coroutine: Coroutine, loop: Optional[asyncio.AbstractEventLoop] = None) -> Coroutine:
    loop = loop or asyncio.get_event_loop()
    return loop.create_task(coroutine)


async def wait_for(coroutine: Coroutine, timeout: int) -> Any:
    coroutine = asyncio.wait_for(coroutine, timeout=timeout)
    try:
        return await coroutine
    except asyncio.TimeoutError:
        pass
    return None
