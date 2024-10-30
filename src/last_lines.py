import io
import os
from pathlib import Path
from typing import Generator, Union


def last_lines(
    path: Union[str, Path],
    buffer_size: int = io.DEFAULT_BUFFER_SIZE,
) -> Generator[str, None, None]:
    with Path(path).open("rb") as f:
        leftover = b""
        remaining = f.seek(0, os.SEEK_END)

        while remaining:
            size_to_read = min(buffer_size, remaining)
            f.seek(remaining - size_to_read)
            remaining -= size_to_read
            buffer = f.read(size_to_read)

            lines = buffer.split(b"\n")
            lines[-1] += leftover
            leftover = lines.pop(0)

            for line in reversed(lines):
                yield line.decode() + "\n"

        yield leftover.decode() + "\n"
