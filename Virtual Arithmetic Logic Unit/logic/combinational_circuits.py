from .logicgates import AND, OR, NOT, NOR, XOR

__all__ = [
    "half_adder",
    "full_adder",
    "four_bit_adder",
    "four_bit_carry_lookahead_adder",
    "half_subtractor",
    "full_subtractor",
    "four_bit_adder_subtractor",
    "BCD_adder",
    "four_bit_by_four_bit_multiplier",
    "four_bit_magnitude_comparator",
    "two_to_four_decoder",
    "three_to_eight_decoder",
    "four_to_sixteen_decoder",
    "four_bit_binary_to_BCD_decoder",
    "binary_to_BCD_decoder",
    "BCD_to_seven_segment_decoder",
    "decimal_to_BCD_encoder",
    "two_to_one_multiplexer",
    "four_to_one_multiplexer",
    "eight_to_one_multiplexer",
    "sixteen_to_one_multiplexer",
]


def half_adder(A: int, B: int) -> tuple[int, int]:
    """
    Carry = A · B \n
    Sum = A ⊕ B
    """
    S = XOR(A, B)
    C = AND(A, B)
    return C, S


def full_adder(A: int, B: int, Cin: int) -> tuple[int, int]:
    """
    Carry = A · B + A·Cin + B·Cin \n
    \t    = (A ⊕ B)Cin + AB \n
    Sum = A ⊕ B ⊕ Cin
    """
    C0, S0 = half_adder(A, B)
    C1, S = half_adder(S0, Cin)
    Cout = OR(C0, C1)
    return Cout, S


def four_bit_adder(
    A3: int, A2: int, A1: int, A0: int, B3: int, B2: int, B1: int, B0: int, Cin: int = 0
) -> tuple[int, int, int, int, int]:
    """ """
    C0, S0 = full_adder(A0, B0, Cin)
    C1, S1 = full_adder(A1, B1, C0)
    C2, S2 = full_adder(A2, B2, C1)
    Cout, S3 = full_adder(A3, B3, C2)
    return Cout, S3, S2, S1, S0


def four_bit_carry_lookahead_adder(
    A3: int,
    A2: int,
    A1: int,
    A0: int,
    B3: int,
    B2: int,
    B1: int,
    B0: int,
    Cin: int = 0,
):
    """ """
    # TODO: Need to implement the logic


def half_subtractor(A: int, B: int) -> tuple[int, int]:
    """
    Borrow = A′B \n
    Difference = A ⊕ B
    """
    Difference = XOR(A, B)
    Borrow = AND(NOT(A), B)
    return Borrow, Difference


def full_subtractor(A: int, B: int, Bin: int) -> tuple[int, int]:
    """
    Borrow = B·Bin + A′·Bin + A′·B
    \t     = (A ⊕ B)′Bin + A′B \n
    Difference = A ⊕ B ⊕ Bin
    """
    B0, D0 = half_subtractor(A, B)
    B1, D = half_subtractor(D0, Bin)
    Bout = OR(B0, B1)
    return Bout, D


def four_bit_adder_subtractor(
    A3: int,
    A2: int,
    A1: int,
    A0: int,
    B3: int,
    B2: int,
    B1: int,
    B0: int,
    M: int,
    Cin: int = 0,
) -> tuple[int, int, int, int, int, int]:
    """ """
    C0, S0 = full_adder(A0, XOR(B0, M), Cin)
    C1, S1 = full_adder(A1, XOR(B1, M), C0)
    C2, S2 = full_adder(A2, XOR(B2, M), C1)
    C3, S3 = full_adder(A3, XOR(B3, M), C2)
    V = XOR(Cout := C3, C2)
    return V, Cout, S3, S2, S1, S0


def BCD_adder(
    A3: int, A2: int, A1: int, A0: int, B3: int, B2: int, B1: int, B0: int, Cin: int = 0
) -> tuple[int, int, int, int, int]:
    """ """
    K, Z8, Z4, Z2, Z1 = four_bit_adder(A3, A2, A1, A0, B3, B2, B1, B0, Cin)

    Cout = OR(K, AND(Z8, Z4), AND(Z8, Z2))
    _, S8, S4, S2, S1 = four_bit_adder(0, Cout, Cout, 0, Z8, Z4, Z2, Z1)
    return Cout, S8, S4, S2, S1


def four_bit_by_four_bit_multiplier(
    A3: int, A2: int, A1: int, A0: int, B3: int, B2: int, B1: int, B0: int
) -> tuple[int, int, int, int, int, int, int, int]:
    """ """
    C0 = AND(A0, B0)
    X3, X2, X1, X0, C1 = four_bit_adder(
        AND(A3, B1),
        AND(A2, B1),
        AND(A1, B1),
        AND(A0, B1),
        0,
        AND(A3, B0),
        AND(A2, B0),
        AND(A1, B0),
    )
    X3, X2, X1, X0, C2 = four_bit_adder(
        AND(A3, B2), AND(A2, B2), AND(A1, B2), AND(A0, B2), X3, X2, X1, X0
    )
    C7, C6, C5, C4, C3 = four_bit_adder(
        AND(A3, B3), AND(A2, B3), AND(A1, B3), AND(A0, B3), X3, X2, X1, X0
    )
    return C7, C6, C5, C4, C3, C2, C1, C0


def four_bit_magnitude_comparator(
    A3: int, A2: int, A1: int, A0: int, B3: int, B2: int, B1: int, B0: int
) -> tuple[int, int, int]:
    """ """
    E = AND(
        wire0 := NOR(g3 := AND(A3, NOT(B3)), l3 := AND(NOT(A3), B3)),
        wire1 := NOR(g2 := AND(A2, NOT(B2)), l2 := AND(NOT(A2), B2)),
        wire2 := NOR(g1 := AND(A1, NOT(B1)), l1 := AND(NOT(A1), B1)),
        NOR(g0 := AND(A0, NOT(B0)), l0 := AND(NOT(A0), B0)),
    )
    G = OR(g3, AND(wire0, g2), AND(wire0, wire1, g1), AND(wire0, wire1, wire2, g0))
    L = OR(l3, AND(wire0, l2), AND(wire0, wire1, l1), AND(wire0, wire1, wire2, l0))
    return G, E, L


def two_to_four_decoder(x: int, y: int, E: int = 1) -> tuple[int, int, int, int]:
    """
    m0 = x′ y′ · E \n
    m1 = x′ y · E \n
    m2 = x y′ · E \n
    m3 = x y · E \n
    """
    m0 = AND(NOT(x), NOT(y), E)
    m1 = AND(NOT(x), y, E)
    m2 = AND(x, NOT(y), E)
    m3 = AND(x, y, E)
    return m0, m1, m2, m3


def three_to_eight_decoder(
    x: int, y: int, z: int, E: int = 1
) -> tuple[int, int, int, int, int, int, int, int]:
    """
    m0 = x′ y′ z′ · E \n
    m1 = x′ y′ z · E \n
    m2 = x′ y z′ · E \n
    m3 = x′ y z · E \n
    m4 = x y′ z′ · E \n
    m5 = x y′ z · E \n
    m6 = x y z′ · E \n
    m7 = x y z · E
    """
    m0 = AND(NOT(x), NOT(y), NOT(z), E)
    m1 = AND(NOT(x), NOT(y), z, E)
    m2 = AND(NOT(x), y, NOT(z), E)
    m3 = AND(NOT(x), y, z, E)
    m4 = AND(x, NOT(y), NOT(z), E)
    m5 = AND(x, NOT(y), z, E)
    m6 = AND(x, y, NOT(z), E)
    m7 = AND(x, y, z, E)
    return m0, m1, m2, m3, m4, m5, m6, m7


def four_to_sixteen_decoder(
    w: int, x: int, y: int, z: int
) -> tuple[
    int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int
]:
    """
    m0 = w′ x′ y′ z′ \n
    m1 = w′ x′ y′ z \n
    m2 = w′ x′ y z′ \n
    m3 = w′ x′ y z \n
    m4 = w′ x y′ z′ \n
    m5 = w′ x y′ z \n
    m6 = w′ x y z′ \n
    m7 = w′ x y z \n
    m8 = w x′ y′ z′ \n
    m9 = w x′ y′ z \n
    m10 = w x′ y z′ \n
    m11 = w x′ y z \n
    m12 = w x y′ z′ \n
    m13 = w x y′ z \n
    m14 = w x y z′ \n
    m15 = w x y z
    """
    m0, m1, m2, m3, m4, m5, m6, m7 = three_to_eight_decoder(x, y, z, NOT(w))
    m8, m9, m10, m11, m12, m13, m14, m15 = three_to_eight_decoder(x, y, z, w)
    return m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15


def four_bit_binary_to_BCD_decoder(
    A: int, B: int, C: int, D: int
) -> tuple[int, int, int, int, int]:
    """
    W = AB + AC \n
    X = AB′C′ \n
    Y = A′B + BC \n
    Z = ABC′ + A′C \n
    E = D
    """
    W = OR(AND(A, B), AND(A, C))
    X = AND(A, NOT(B), NOT(C))
    Y = OR(AND(NOT(A), B), AND(B, C))
    Z = OR(AND(A, B, NOT(C)), AND(NOT(A), C))
    E = D
    return W, X, Y, Z, E


def binary_to_BCD_decoder(
    B7: int, B6: int, B5: int, B4: int, B3: int, B2: int, B1: int, B0: int
) -> tuple[int, int, int, int, int, int, int, int, int, int]:
    """ """

    # * Adds 3 (0011) to the shift value if it exceeds 4 (0100).
    def dabbler(I3: int, I2: int, I1: int, I0: int) -> tuple[int, int, int, int]:
        O3 = OR(AND(I3, NOT(I2), NOT(I1)), AND(NOT(I3), I2, I0), AND(NOT(I3), I2, I1))
        O2 = OR(AND(NOT(I3), I2, NOT(I1), NOT(I0)), AND(I3, NOT(I2), NOT(I1), I0))
        O1 = OR(
            x := AND(I3, NOT(I2), NOT(I1), NOT(I0)),
            AND(NOT(I3), I1, I0),
            AND(NOT(I3), NOT(I2), I1),
        )
        O0 = OR(x, AND(NOT(I3), I2, I1, NOT(I0)), AND(NOT(I3), NOT(I2), I0))
        return O3, O2, O1, O0

    w0, w1, w2, w3 = dabbler(0, B7, B6, B5)
    x0, x1, x2, x3 = dabbler(w1, w2, w3, B4)
    y0, y1, y2, y3 = dabbler(x1, x2, x3, B3)
    z0, z1, z2, z3 = dabbler(0, w0, x0, y0)
    z4, z5, z6, z7 = dabbler(y1, y2, y3, B2)
    P9 = z0
    P8, P7, P6, P5 = dabbler(z1, z2, z3, z4)
    P4, P3, P2, P1 = dabbler(z5, z6, z7, B1)
    P0 = B0
    return P9, P8, P7, P6, P5, P4, P3, P2, P1, P0


def BCD_to_seven_segment_decoder(
    D: int, C: int, B: int, A: int
) -> tuple[int, int, int, int, int, int, int]:
    """
    a = C′A′+ B + CA + D \n
    b = C′ + B′A′ + BA \n
    c = B′ + A + C \n
    d = C′A′ + C′B + CB′A + BA′ + D \n
    e = C′A′ + BA′ \n
    f = B′A′ + CB′ + CA′ + D \n
    g = C′B + CB′ + D + BA′ \n
    """
    a = OR(wire0 := AND(NOT(C), NOT(A)), B, AND(C, A), D)
    b = OR(NOT(C), wire1 := AND(NOT(B), NOT(A)), AND(B, A))
    c = OR(NOT(B), A, C)
    d = OR(
        wire0,
        wire2 := AND(NOT(C), B),
        AND(C, NOT(B), A),
        wire3 := AND(B, NOT(A)),
        D,
    )
    e = OR(wire0, wire3)
    f = OR(
        wire1,
        x4 := AND(C, NOT(B)),
        AND(C, NOT(A)),
        D,
    )
    g = OR(wire2, x4, D, wire3)
    return a, b, c, d, e, f, g


def decimal_to_BCD_encoder(
    D1: int,
    D2: int,
    D3: int,
    D4: int,
    D5: int,
    D6: int,
    D7: int,
    D8: int,
    D9: int,
) -> tuple[
    int,
    int,
    int,
    int,
]:
    """
    D = D8 + D9 \n
    C = D4 + D5 + D6 + D7 \n
    B = D2 + D3 + D6 + D7 \n
    A = D1 + D3 + D5 + D7 + D9
    """
    D = OR(D8, D9)
    C = OR(D4, D5, D6, D7)
    B = OR(D2, D3, D6, D7)
    A = OR(D1, D3, D5, D7, D9)

    return D, C, B, A


def two_to_one_multiplexer(I0: int, I1: int, S: int, E: int = 1) -> int:
    Y = OR(AND(I0, NOT(S), E), AND(I1, S, E))
    return Y


def four_to_one_multiplexer(
    I0: int, I1: int, I2: int, I3: int, S1: int, S0: int, E: int = 1
) -> int:
    """ """
    Y = OR(
        AND(I0, NOT(S1), NOT(S0), E),
        AND(I1, NOT(S1), S0, E),
        AND(I2, S1, NOT(S0), E),
        AND(I3, S1, S0, E),
    )
    return Y


def eight_to_one_multiplexer(
    I0: int,
    I1: int,
    I2: int,
    I3: int,
    I4: int,
    I5: int,
    I6: int,
    I7: int,
    S2: int,
    S1: int,
    S0: int,
    E: int = 1,
) -> int:
    """ """
    Y = OR(
        AND(I0, NOT(S2), NOT(S1), NOT(S0), E),
        AND(I1, NOT(S2), NOT(S1), S0, E),
        AND(I2, NOT(S2), S1, NOT(S0), E),
        AND(I3, NOT(S2), S1, S0, E),
        AND(I4, S2, NOT(S1), NOT(S0), E),
        AND(I5, S2, NOT(S1), S0, E),
        AND(I6, S2, S1, NOT(S0), E),
        AND(I7, S2, S1, S0, E),
    )
    return Y


def sixteen_to_one_multiplexer(
    I0: int,
    I1: int,
    I2: int,
    I3: int,
    I4: int,
    I5: int,
    I6: int,
    I7: int,
    I8: int,
    I9: int,
    I10: int,
    I11: int,
    I12: int,
    I13: int,
    I14: int,
    I15: int,
    S3: int,
    S2: int,
    S1: int,
    S0: int,
    E: int = 1,
) -> int:
    """ """
    Y = OR(
        AND(I0, NOT(S3), NOT(S2), NOT(S1), NOT(S0), E),
        AND(I1, NOT(S3), NOT(S2), NOT(S1), S0, E),
        AND(I2, NOT(S3), NOT(S2), S1, NOT(S0), E),
        AND(I3, NOT(S3), NOT(S2), S1, S0, E),
        AND(I4, NOT(S3), S2, NOT(S1), NOT(S0), E),
        AND(I5, NOT(S3), S2, NOT(S1), S0, E),
        AND(I6, NOT(S3), S2, S1, NOT(S0), E),
        AND(I7, NOT(S3), S2, S1, S0, E),
        AND(I8, S3, NOT(S2), NOT(S1), NOT(S0), E),
        AND(I9, S3, NOT(S2), NOT(S1), S0, E),
        AND(I10, S3, NOT(S2), S1, NOT(S0), E),
        AND(I11, S3, NOT(S2), S1, S0, E),
        AND(I12, S3, S2, NOT(S1), NOT(S0), E),
        AND(I13, S3, S2, NOT(S1), S0, E),
        AND(I14, S3, S2, S1, NOT(S0), E),
        AND(I15, S3, S2, S1, S0, E),
    )
    return Y
