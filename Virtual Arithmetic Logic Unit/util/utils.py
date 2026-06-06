__all__ = ["binary", "decimal", "combinations", "expression"]


def binary(dec: int, word: int = 4) -> tuple[int, ...]:
    """
    Converts a decimal number to its binary equivalent as a tuple of individual bits.
    """
    bin = tuple(int(bit) for bit in format(dec, f"0{word}b"))
    return bin


def decimal(bin: tuple[int, ...]) -> None:
    """
    Converts a tuple of binary bits to its decimal equivalent and prints it.
    """
    if any(bit not in (0, 1) for bit in bin):
        raise ValueError("Inputs must be binary (0 or 1).")
    dec = int("".join(str(bit) for bit in bin), 2)
    print(dec)


def combinations(bits: int) -> str:
    """
    Generate all combinations of binary sequences for a given number of bits.
    """
    sequences = [binary(num, bits) for num in range(2**bits)]
    return "\n".join(" ".join(str(bit) for bit in seq) for seq in sequences)


def expression(inputs: str | list[str] | tuple[str, ...], row_index: int) -> str:
    """
    Converts a row index to its corresponding Boolean expression based on the input variable names.
    """
    expr = [
        f"{symbol}{'′' if not bit else ''}"
        for symbol, bit in zip(inputs, binary(row_index, len(inputs)))
    ]
    return "".join(expr)
