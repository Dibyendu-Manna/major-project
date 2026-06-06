__all__ = ["AND", "OR", "NOT", "BUF", "NAND", "NOR", "XOR", "XNOR"]


def AND(x: int, y: int, *z: int) -> int:
    """
    x · y · z ...
    """
    if not z:
        if x not in (0, 1) or y not in (0, 1):
            raise ValueError("Inputs must be binary (0 or 1).")
        return int(x and y)
    else:
        return AND(AND(x, y), *z)


def OR(x: int, y: int, *z: int) -> int:
    """
    x + y + z ...
    """
    if not z:
        if x not in (0, 1) or y not in (0, 1):
            raise ValueError("Inputs must be binary (0 or 1).")
        return int(x or y)
    else:
        return OR(OR(x, y), *z)


def NOT(x: int) -> int:
    """
    x′
    """
    if x not in (0, 1):
        raise ValueError("Inputs must be binary (0 or 1).")
    return int(not x)


def BUF(x: int) -> int:
    """
    x
    """
    if x not in (0, 1):
        raise ValueError("Inputs must be binary (0 or 1).")
    return int(x)


def NAND(x: int, y: int, *z: int) -> int:
    """
    (x · y · z ... )′
    """
    if not z:
        if x not in (0, 1) or y not in (0, 1):
            raise ValueError("Inputs must be binary (0 or 1).")
        return int(NOT(AND(x, y)))
    else:
        return int(NOT(AND(x, y, *z)))


def NOR(x: int, y: int, *z: int) -> int:
    """
    (x + y + z ...)′
    """
    if not z:
        if x not in (0, 1) or y not in (0, 1):
            raise ValueError("Inputs must be binary (0 or 1).")
        return int(NOT(OR(x, y)))
    else:
        return int(NOT(OR(x, y, *z)))


def XOR(x: int, y: int, *z: int) -> int:
    """
    x ⊕ y ⊕ z ...
        xy′z′ ... + x′yz′ ... + x′y′z ... + xyz ...
    """
    if not z:
        if x not in (0, 1) or y not in (0, 1):
            raise ValueError("Inputs must be binary (0 or 1).")
        return int(OR(AND(x, NOT(y)), AND(NOT(x), y)))
    else:
        return XOR(XOR(x, y), *z)


def XNOR(x: int, y: int, *z: int) -> int:
    """
    (x ⊙ y ⊙ z ...)
        (x ⊕ y ⊕ z ...)′
        xyz ... + x′y′z′ ...
    """
    if not z:
        if x not in (0, 1) or y not in (0, 1):
            raise ValueError("Inputs must be binary (0 or 1).")
        return int(OR(AND(x, y), AND(NOT(x), NOT(y))))
    else:
        return XNOR(XNOR(x, y), *z)
