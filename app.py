import cmath
import json
import pydoc
import traceback
from typing import Any
from typing import Callable
from typing import Dict

tasks = {}


# 1. кто тут декоратор?
def task(name):
    # 2. почему не используется functools.wraps?
    def internal(func):
        func.__task_name__ = name
        tasks[name] = func
        return func

    return internal


@task("3.09")
# 3. почему в аргументах сначала стоит звёздочка?
def task_0309(*, a: int, b: int, c: int) -> Dict[str, str]:
    """
    Calculates the roots for quadratic equation:

    ```
    ax**2 + bx + c = 0
    ```

    Values of a, b, c MUST be integers.

    Can into complex hence values are strings.
    """

    d = cmath.sqrt(b ** 2 - 4 * a * c)
    if not a:
        if not b:
            if not c:
                x1 = x2 = 0
            else:
                x1 = x2 = float("nan")  # 4. что это такое?
        else:
            x1 = x2 = -c / b
    else:
        # 5. почему используется list?
        x1, x2 = list(map(lambda sign: (-b + sign * d) / (2 * a), [1, -1]))

    result = {
        "x1": str(x1),  # 6. почему значения конвертятся в строку тут?
        "x2": str(x2),
    }

    return result


@task("3.01")
def task_0301(*, name: str) -> str:
    """
    Returns "Hello, [{name}]!" for given name.
    """

    result = f"Hello, [{name}]!"
    return result


class MyAppError(RuntimeError):
    code = "500 Internal Server Error"


class TaskError(MyAppError):
    code = "400 Bad Request"

    def __init__(self, *args, task_name):
        self._task_name = task_name  # почему подчёркивание?
        super().__init__(*args)  # почему?


class UnknownTaskError(TaskError):
    code = "404 Not Found"

    def __str__(self):
        return f"Unknown task: '{self._task_name}'."


class InvalidTaskUsageError(TaskError):
    def __str__(self):
        tf = tasks[self._task_name]  # безопасен ли такой код?
        doc = pydoc.render_doc(tf)  # почему?
        return f"Invalid usage of task '{self._task_name}'.\nDocumentation:\n{doc}"


# почему?
def get_task_func(task_name: str) -> Callable:
    try:
        return tasks[task_name]
    except KeyError as err:
        raise UnknownTaskError(task_name=task_name) from err


# почему?
def run_task(task_func: Callable, args: Dict[str, Any]) -> Any:
    try:
        return task_func(**args)
    except TypeError as err:
        # что за новый магический атрибут?
        raise InvalidTaskUsageError(task_name=task_func.__task_name__) from err


# почему?
def get_task_data(environ: Dict):
    content = read_content(environ)
    return content["task"], content["args"]


# почему?
def read_content(environ: Dict) -> Dict:
    content_length_raw = environ.get("CONTENT_LENGTH")
    if not content_length_raw:
        return {}

    content_length = int(content_length_raw)
    client_stream = environ["wsgi.input"]
    content = json.loads(client_stream.read(content_length))

    return content


def compose_payload(task_name, *, result=None, error=None) -> bytes:
    payload = {
        "task": task_name
    }

    # почему?
    if result:
        payload["result"] = result
    # почему?
    if error:
        payload["error"] = str(error)

    return json.dumps(payload).encode()


def webapp(environ, start_response):
    status = "200 OK"

    try:
        task_name, task_args = get_task_data(environ)
        task_func = get_task_func(task_name)
        result = run_task(task_func, task_args)

        payload = compose_payload(task_name, result=result)

    except TaskError as err:
        status = err.code
        task_name = err._task_name
        payload = compose_payload(task_name, error=err)

    except MyAppError as err:
        status = err.code
        payload = compose_payload(None, error=err)

    except Exception:
        traceback.print_exc()
        status = "500 Internal Server Error"
        payload = compose_payload(None, error=traceback.format_exc())

    # всегда ли эта WSGI-программа отправляет клиенту JSON?
    start_response(
        status,
        [
            ("content-type", "application/json; charset=utf-8"),
        ],
    )

    # почему?
    yield payload
