from re import fullmatch
from typing import TypedDict
from .utils import binary

Canonical = TypedDict(
    "Canonical",
    {
        "function": str,
        "minterms": dict[int, str],
        "maxterms": dict[int, str],
        "don't cares": dict[int, str],
        "m": str,
        "M": str,
        "d": str,
        "sop": str,
        "pos": str,
    },
)

__all__ = ["canonical"]


def canonical(truth_table: str, sep: str = "|") -> list[Canonical]:
    """
    Synthesize canonical forms (minterms, maxterms, and don't cares) from a truth table.
    """
    if sep.isspace():
        raise ValueError("Separator cannot contain space(s).")
    rows = [row.strip() for row in truth_table.strip().splitlines() if row.strip()]
    if not rows:
        raise ValueError("Truth-Table is empty.")
    if not fullmatch(r"^[^|]+\|[^|]+$", rows[0].replace(" ", "")):
        raise SyntaxError("Invalid header format.")
    inputs, outputs = [header.strip().split() for header in rows[0].split(sep)]
    if len(rows) - 1 != 2 ** len(inputs):
        raise ValueError("Number of rows does not match number of input combinations.")
    canonicals: list[Canonical] = [
        {
            "function": function,
            "minterms": {},
            "maxterms": {},
            "don't cares": {},
            "m": "",
            "M": "",
            "d": "",
            "sop": "",
            "pos": "",
        }
        for function in outputs
    ]
    sop: list[list[str]] = [[] for _ in outputs]
    pos: list[list[str]] = [[] for _ in outputs]
    F = f"F({','.join(inputs)})"
    for index, row in enumerate(rows[1:]):
        if not fullmatch(
            rf"^[01]{{{len(inputs)}}}{'\\' if sep == '|' else ''}{sep}[01Xx]{{{len(outputs)}}}$",
            row.replace(" ", ""),
        ):
            raise SyntaxError(f"Invalid row format: {row}")
        combinations, values = [io.strip().split() for io in row.split(sep)]
        for i, value in enumerate(values):
            if "".join(str(bit) for bit in binary(index, len(inputs))) != "".join(
                combinations
            ):
                raise ValueError(
                    f"Binary combination does not match row index in row: {row}"
                )
            if value == "1":
                canonicals[i]["minterms"][index] = "".join(combinations)
                expr = "".join(
                    f"{symbol}{'′' if not int(bit) else ''}"
                    for symbol, bit in zip(inputs, combinations)
                )
                sop[i].append(expr)
            elif value == "0":
                canonicals[i]["maxterms"][index] = "".join(combinations)
                expr = f"({
                    ' + '.join(
                        f'{symbol}{'′' if int(bit) else ''}'
                        for symbol, bit in zip(inputs, combinations)
                    )
                })"
                pos[i].append(expr)
            elif value in ("x", "X"):
                canonicals[i]["don't cares"][index] = "".join(combinations)
    for i, c in enumerate(canonicals):
        c["m"] = f"∑ m({','.join(str(key) for key in c['minterms'].keys())})"
        c["M"] = f"∏ M({','.join(str(key) for key in c['maxterms'].keys())})"
        c["d"] = f"d({','.join(str(key) for key in c["don't cares"].keys())})"
        c["sop"] = f"{F} = {' + '.join(sop[i])}"
        c["pos"] = f"{F} = {' '.join(pos[i])}"
    return canonicals
