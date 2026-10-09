from contextlib import (
    contextmanager,
    redirect_stdout,
    redirect_stderr,
    suppress,
    chdir,  # Python 3.11+
)
from decimal import Decimal, localcontext
from pathlib import Path
from tempfile import TemporaryDirectory, TemporaryFile
from threading import Lock, RLock, Semaphore, Condition
from zipfile import ZipFile, ZIP_DEFLATED
import io
import mmap
import socket
import threading
import warnings


DATA_FILE = Path("with_example_data.txt")


def file_examples():
    # 1. Read a text file. `with` closes the file automatically at block exit.
    DATA_FILE.write_text("Hello from Python!\nSecond line.\n", encoding="utf-8")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        print("Read files:", f.read().strip())

    # 2. Write to a file. Mode "w" creates the file or replaces its contents.
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write("This text replaced the old contents.\n")
    print("Write files: wrote new contents")

    # 3. Append to a file. Mode "a" adds text to the end.
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write("This line was appended.\n")
    print("Append to files:", DATA_FILE.read_text(encoding="utf-8").strip())


def threading_examples():
    # 4. Thread lock: only one thread at a time can enter the protected block.
    lock = Lock()
    with lock:
        print("Thread lock: shared state would be updated safely here")

    # 5. Reentrant lock: the same thread may acquire the lock more than once.
    rlock = RLock()
    with rlock:
        with rlock:
            print("Reentrant lock: same thread acquired it twice")

    # 6. Semaphore: limits how many threads may enter a block simultaneously.
    semaphore = Semaphore(2)
    with semaphore:
        print("Semaphore: inside a limited-capacity section")

    # 7. Condition: acquires its associated lock; often used with wait()/notify().
    condition = Condition()
    with condition:
        # Real concurrent programs usually call condition.wait() here when a
        # predicate is false, and another thread calls condition.notify().
        print("Condition variable: condition lock is held")


def temporary_resource_examples():
    # 8. Temporary directory: the directory and its contents are removed on exit.
    with TemporaryDirectory() as folder:
        temp_path = Path(folder) / "sample.txt"
        temp_path.write_text("temporary", encoding="utf-8")
        print("Temporary directory: created", temp_path.name)
    # The temporary directory no longer exists here.

    # 9. Temporary file: the file is closed and typically removed on exit.
    with TemporaryFile(mode="w+t", encoding="utf-8") as f:
        f.write("temporary file contents")
        f.seek(0)
        print("Temporary file:", f.read())

    # 10. Memory mapping: maps a file into memory; useful for large/binary files.
    # The file must have at least one byte for this example.
    with open(DATA_FILE, "r+b") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
            print("Memory mapping: first bytes =", mm[:10])


def decimal_example():
    # 11. localcontext: temporarily changes decimal arithmetic settings.
    with localcontext() as ctx:
        ctx.prec = 4
        print("Decimal precision:", Decimal("1") / Decimal("7"))
    # The prior decimal context is restored after the block.


def output_and_exception_examples():
    # 12. Redirect stdout: capture print() output in a StringIO buffer.
    stdout_buffer = io.StringIO()
    with redirect_stdout(stdout_buffer):
        print("This print is captured instead of shown on the console.")
    print("Redirect stdout:", stdout_buffer.getvalue().strip())

    # 13. Redirect stderr: capture error/status messages written to stderr.
    stderr_buffer = io.StringIO()
    with redirect_stderr(stderr_buffer):
        import sys
        print("This error message is captured.", file=sys.stderr)
    print("Redirect stderr:", stderr_buffer.getvalue().strip())

    # 14. Suppress exceptions: ignore only the listed exception types.
    with suppress(FileNotFoundError):
        Path("a_file_that_does_not_exist_12345.txt").unlink()
    print("Suppress exceptions: missing-file error was ignored")

    # Another standard-library context manager: capture warnings temporarily.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warnings.warn("Example warning", UserWarning)
    print("Warnings captured:", len(caught))


def directory_example():
    # 15. Change working directory temporarily (Python 3.11+).
    original_dir = Path.cwd()
    with TemporaryDirectory() as folder:
        with chdir(folder):
            print("Change working directory:", Path.cwd() != original_dir)
        # Current directory is restored when the `chdir` block exits.


def network_and_archive_examples():
    # 16. Network socket: `with` closes the socket even if an error occurs.
    # This opens a local socket object but does not connect to any server.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Network connection: created socket", s.fileno() >= 0)

    # 17. Archive file: `with` closes the ZIP archive after use.
    zip_path = Path("with_example_archive.zip")
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as z:
        z.write(DATA_FILE, arcname=DATA_FILE.name)
    with ZipFile(zip_path, "r") as z:
        print("Archive files:", z.namelist())
    # Remove the example archive so it does not clutter the directory.
    zip_path.unlink(missing_ok=True)


def custom_context_manager_example():
    # Context managers can perform custom setup and cleanup.
    @contextmanager
    def example_scope():
        print("Custom context manager: setup")
        try:
            yield
        finally:
            print("Custom context manager: cleanup")

    with example_scope():
        print("Custom context manager: doing work")


def third_party_templates():
    # 18. Database transaction: exact behavior depends on the database driver.
    # Example with sqlite3 (standard library):
    import sqlite3
    with sqlite3.connect(":memory:") as connection:
        # For sqlite3, leaving the block commits on success and rolls back on
        # an exception. The connection itself is not necessarily closed by
        # the context manager, so close it separately when finished.
        connection.execute("CREATE TABLE example (value TEXT)")
        connection.execute("INSERT INTO example VALUES (?)", ("hello",))
        rows = connection.execute("SELECT value FROM example").fetchall()
        print("Database transaction:", rows)
    connection.close()

    # 19. Database cursor: supported by some drivers (for example psycopg).
    # Uncomment after installing/configuring a compatible driver:
    #
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT 1")
    #     print(cursor.fetchone())
    #
    # Not every driver's cursor supports `with`.

    # 20. HTTP response: `requests` is third-party. Install with `pip install requests`.
    # `with` ensures the streamed response is closed.
    #
    # import requests
    # with requests.get("https://example.com", stream=True, timeout=10) as response:
    #     response.raise_for_status()
    #     print(response.status_code)

    # 21. Async resource cleanup: requires aiofiles and an async function.
    # Install with `pip install aiofiles`.
    #
    # import asyncio
    # import aiofiles
    #
    # async def read_async():
    #     async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
    #         return await f.read()
    #
    # print(asyncio.run(read_async()))


def main():
    print("\n--- Files ---")
    file_examples()
    print("\n--- Thread synchronization ---")
    threading_examples()
    print("\n--- Temporary resources and memory mapping ---")
    temporary_resource_examples()
    print("\n--- Decimal context ---")
    decimal_example()
    print("\n--- Output and exception handling ---")
    output_and_exception_examples()
    print("\n--- Working directory ---")
    directory_example()
    print("\n--- Network and archive ---")
    network_and_archive_examples()
    print("\n--- Custom context manager ---")
    custom_context_manager_example()
    print("\n--- Database and optional-library templates ---")
    third_party_templates()
    print("\nDone. The reusable text file is:", DATA_FILE.resolve())


if __name__ == "__main__":
    main()
