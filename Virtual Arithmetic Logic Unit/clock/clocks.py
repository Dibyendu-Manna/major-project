from collections.abc import Generator

__all__ = ["binary_clock"]


def binary_clock(cycle: int | None = None) -> Generator[int, None, None]:
    """ """
    cycles_elapsed = 0
    while True:
        yield from (1, 0)
        cycles_elapsed += 1
        if cycle is not None and cycles_elapsed == cycle:
            break
