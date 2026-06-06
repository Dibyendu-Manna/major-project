from .logicgates import AND, OR, NOT, NAND, NOR, XOR, XNOR

from .combinational_circuits import (
    half_adder,
    full_adder,
    four_bit_adder_subtractor,
    four_bit_magnitude_comparator,
    two_to_one_multiplexer,
    four_to_one_multiplexer,
    eight_to_one_multiplexer,
)

__all__ = ["FourBitALU"]


class FourBitALU:
    """ """

    def __init__(self) -> None:
        self.A3, self.A2, self.A1, self.A0 = 0, 0, 0, 0
        self.B3, self.B2, self.B1, self.B0 = 0, 0, 0, 0
        self.CIN = 0
        self.G1, self.G0 = 0, 0
        self.F2, self.F1, self.F0 = 0, 0, 0
        (
            self.S,
            self.CF,
            (self.Y3, self.Y2, self.Y1, self.Y0),
            self.Z,
            self.P,
            self.V,
        ) = self(  # * Initializing the ALU by performing calculation with all input pins assign to 0.
            (self.A3, self.A2, self.A1, self.A0),
            (self.B3, self.B2, self.B1, self.B0),
            self.G1,
            self.G0,
            self.F2,
            self.F1,
            self.F0,
            self.CIN,
        )

    def __str__(self) -> str:
        return (
            "    ┌────────────┐\n"
            f"{self.F2} ──┤F2        G1├── {self.G1}\n"
            f"{self.F1} ──┤F1        G0├── {self.G0}\n"
            f"{self.F0} ──┤F0         V├── {self.V}\n"
            f"{self.CIN} ──┤CIN        P├── {self.P}\n"
            f"{self.B3} ──┤B3         Z├── {self.Z}\n"
            f"{self.B2} ──┤B2        Y0├── {self.Y0}\n"
            f"{self.B1} ──┤B1        Y1├── {self.Y1}\n"
            f"{self.B0} ──┤B0        Y2├── {self.Y2}\n"
            f"{self.A3} ──┤A3        Y3├── {self.Y3}\n"
            f"{self.A2} ──┤A2        CF├── {self.CF}\n"
            f"{self.A1} ──┤A1         S├── {self.S}\n"
            f"{self.A0} ──┤A0          │\n"
            "    └────────────┘\n"
        )

    def __call__(
        self,
        ACC: tuple[int, int, int, int],
        B: tuple[int, int, int, int],
        G1: int,
        G0: int,
        F2: int,
        F1: int,
        F0: int,
        CIN: int = 0,
    ) -> tuple[int, int, tuple[int, int, int, int], int, int, int]:
        self.A3, self.A2, self.A1, self.A0 = ACC
        self.B3, self.B2, self.B1, self.B0 = B
        self.V, C, S3, S2, S1, S0 = four_bit_adder_subtractor(
            two_to_one_multiplexer(
                self.A3,
                0,  # *  0 - ACC = ~ACC or 2's complement of ACC.
                # *  0 is only passed when NEG is performed i.e., F2 F1 = 1 1.
                AND(F2, F1),
            ),
            two_to_one_multiplexer(self.A2, 0, AND(F2, F1)),
            two_to_one_multiplexer(self.A1, 0, AND(F2, F1)),
            two_to_one_multiplexer(self.A0, 0, AND(F2, F1)),
            two_to_one_multiplexer(
                self.B3, four_to_one_multiplexer(0, 0, self.A3, 0, F1, F0), F2
            ),
            two_to_one_multiplexer(
                self.B2, four_to_one_multiplexer(0, 0, self.A2, 0, F1, F0), F2
            ),
            two_to_one_multiplexer(
                self.B1, four_to_one_multiplexer(0, 0, self.A1, 0, F1, F0), F2
            ),
            two_to_one_multiplexer(
                self.B0, four_to_one_multiplexer(0, 1, self.A0, 0, F1, F0), F2
            ),
            SUB
            := OR(  # * Determining wether the SUB operation is to be performed or not and passing it as M.
                AND(F1, NOT(F0)), AND(NOT(F2), F1), AND(F2, NOT(F1), F0)
            ),
            eight_to_one_multiplexer(0, CIN, 1, XOR(1, CIN), 1, 1, 1, 0, F2, F1, F0),
        )
        self.S = AND(NOT(C), SUB, NOT(G1), NOT(G0))
        _, _, N3, N2, N1, N0 = (
            four_bit_adder_subtractor(  # * Performing NEG to negative 2's complement values to get original values.
                0, 0, 0, 0, S3, S2, S1, S0, 1, 1
            )
        )
        # * Perform POPCNT by adding all the 1's in ACC.
        P1, P0 = full_adder(self.A2, self.A1, self.A0)
        wire0, P0 = half_adder(P0, self.A3)
        P2, P1 = half_adder(P1, wire0)
        # * Comparing A and B for performing max(ACC, B).
        GRT, EQ, _ = four_bit_magnitude_comparator(
            self.A3, self.A2, self.A1, self.A0, self.B3, self.B2, self.B1, self.B0
        )
        self.Y3 = four_to_one_multiplexer(
            two_to_one_multiplexer(
                two_to_one_multiplexer(S3, N3, XOR(self.S, AND(F2, F1, NOT(F0)))),
                two_to_one_multiplexer(self.B3, self.A3, OR(GRT, EQ)),
                AND(F2, F1, F0),
            ),
            eight_to_one_multiplexer(
                AND(self.A3, self.B3),
                OR(self.A3, self.B3),
                NOT(self.A3),
                NAND(self.A3, self.B3),
                NOR(self.A3, self.B3),
                XOR(self.A3, self.B3),
                XNOR(self.A3, self.B3),
                0,
                F2,
                F1,
                F0,
            ),
            eight_to_one_multiplexer(
                self.A2, 0, self.A3, self.A2, self.A0, self.A2, CIN, self.A0, F2, F1, F0
            ),
            int(),
            G1,
            G0,
        )
        self.Y2 = four_to_one_multiplexer(
            two_to_one_multiplexer(
                two_to_one_multiplexer(S2, N2, XOR(self.S, AND(F2, F1, NOT(F0)))),
                two_to_one_multiplexer(self.B2, self.A2, OR(GRT, EQ)),
                AND(F2, F1, F0),
            ),
            eight_to_one_multiplexer(
                AND(self.A2, self.B2),
                OR(self.A2, self.B2),
                NOT(self.A2),
                NAND(self.A2, self.B2),
                NOR(self.A2, self.B2),
                XOR(self.A2, self.B2),
                XNOR(self.A2, self.B2),
                P2,
                F2,
                F1,
                F0,
            ),
            eight_to_one_multiplexer(
                self.A1,
                self.A3,
                self.A3,
                self.A1,
                self.A3,
                self.A1,
                self.A3,
                self.A1,
                F2,
                F1,
                F0,
            ),
            int(),
            G1,
            G0,
        )
        self.Y1 = four_to_one_multiplexer(
            two_to_one_multiplexer(
                two_to_one_multiplexer(S1, N1, XOR(self.S, AND(F2, F1, NOT(F0)))),
                two_to_one_multiplexer(self.B1, self.A1, OR(GRT, EQ)),
                AND(F2, F1, F0),
            ),
            eight_to_one_multiplexer(
                AND(self.A1, self.B1),
                OR(self.A1, self.B1),
                NOT(self.A1),
                NAND(self.A1, self.B1),
                NOR(self.A1, self.B1),
                XOR(self.A1, self.B1),
                XNOR(self.A1, self.B1),
                P1,
                F2,
                F1,
                F0,
            ),
            eight_to_one_multiplexer(
                self.A0,
                self.A2,
                self.A2,
                self.A0,
                self.A2,
                self.A0,
                self.A2,
                self.A2,
                F2,
                F1,
                F0,
            ),
            int(),
            G1,
            G0,
        )
        self.Y0 = four_to_one_multiplexer(
            two_to_one_multiplexer(
                two_to_one_multiplexer(S0, N0, XOR(self.S, AND(F2, F1, NOT(F0)))),
                two_to_one_multiplexer(self.B0, self.A0, OR(GRT, EQ)),
                AND(F2, F1, F0),
            ),
            eight_to_one_multiplexer(
                AND(self.A0, self.B0),
                OR(self.A0, self.B0),
                NOT(self.A0),
                NAND(self.A0, self.B0),
                NOR(self.A0, self.B0),
                XOR(self.A0, self.B0),
                XNOR(self.A0, self.B0),
                P0,
                F2,
                F1,
                F0,
            ),
            eight_to_one_multiplexer(
                0, self.A1, self.A1, self.A3, self.A1, CIN, self.A1, self.A3, F2, F1, F0
            ),
            int(),
            G1,
            G0,
        )
        self.CF = four_to_one_multiplexer(
            C,
            0,
            two_to_one_multiplexer(self.A3, self.A0, F0, NOR(NOT(F2), F1)),
            int(),
            G1,
            G0,
        )
        self.Z = NOR(self.Y3, self.Y2, self.Y1, self.Y0)
        self.P = XNOR(self.Y3, self.Y2, self.Y1, self.Y0)
        self.CIN = CIN
        self.G1, self.G0 = G1, G0
        self.F2, self.F1, self.F0 = F2, F1, F0
        return (
            self.S,
            self.CF,
            (self.Y3, self.Y2, self.Y1, self.Y0),
            self.Z,
            self.P,
            self.V,
        )
