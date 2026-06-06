from .logicgates import AND, OR, NOT
from .combinational_circuits import four_to_one_multiplexer
from .sequential_circuits import DFlipFlop, JKFlipFlop

# ! Still in development, Not fully tested yet
__all__ = [
    "FourBitRegister",
    "FourBitShiftRegister",
    "FourBitUniversalShiftRegister",
    "FourBitBinaryRippleCounter",
    "BCDRippleCounter",
]


class FourBitRegister:
    def __init__(self, edge: str) -> None:
        self.D_FF3, self.D_FF2, self.D_FF1, self.D_FF0 = (
            DFlipFlop(edge),
            DFlipFlop(edge),
            DFlipFlop(edge),
            DFlipFlop(edge),
        )

    def __call__(
        self, I3: int, I2: int, I1: int, I0: int, Clk: int, Load: int
    ) -> tuple[int, int, int, int]:
        A3, _ = self.D_FF3(
            OR(AND(X2 := NOT(X1 := NOT(Load)), I3), AND(X1, self.D_FF3.Q)), Clk
        )
        A2, _ = self.D_FF2(OR(AND(self.D_FF2.Q, X1), AND(I2, X2)), Clk)
        A1, _ = self.D_FF1(OR(AND(self.D_FF1.Q, X1), AND(I1, X2)), Clk)
        A0, _ = self.D_FF0(OR(AND(self.D_FF0.Q, X1), AND(I0, X2)), Clk)
        return A3, A2, A1, A0


class FourBitShiftRegister:
    def __init__(self, edge: str) -> None:
        self.D_FF3, self.D_FF2, self.D_FF1, self.D_FF0 = (
            DFlipFlop(edge),
            DFlipFlop(edge),
            DFlipFlop(edge),
            DFlipFlop(edge),
        )

    def __call__(self, SI: int, Clk: int) -> int:
        Q3, _ = self.D_FF3(SI, Clk)
        Q2, _ = self.D_FF2(Q3, Clk)
        Q1, _ = self.D_FF1(Q2, Clk)
        SO, _ = self.D_FF0(Q1, Clk)
        return SO


class FourBitUniversalShiftRegister:
    def __init__(self, edge: str) -> None:
        self.D_FF3, self.D_FF2, self.D_FF1, self.D_FF0 = (
            DFlipFlop(edge),
            DFlipFlop(edge),
            DFlipFlop(edge),
            DFlipFlop(edge),
        )

    def __call__(
        self,
        I3: int,
        I2: int,
        I1: int,
        I0: int,
        S1: int,
        S0: int,
        Serial_Input_for_Shift_Right: int,
        Serial_Input_for_Shift_Left: int,
        Clk: int,
        Clear_b: int = 0,
    ) -> tuple[int, int, int, int]:
        A0, _ = self.D_FF0(
            four_to_one_multiplexer(
                self.D_FF0.Q, self.D_FF1.Q, Serial_Input_for_Shift_Left, I0, S1, S0
            ),
            Clk,
            Clear_b,
        )
        A1, _ = self.D_FF1(
            four_to_one_multiplexer(
                self.D_FF1.Q, self.D_FF2.Q, self.D_FF0.Q, I1, S1, S0
            ),
            Clk,
            Clear_b,
        )
        A2, _ = self.D_FF2(
            four_to_one_multiplexer(
                self.D_FF2.Q, self.D_FF3.Q, self.D_FF1.Q, I2, S1, S0
            ),
            Clk,
            Clear_b,
        )
        A3, _ = self.D_FF3(
            four_to_one_multiplexer(
                self.D_FF3.Q, Serial_Input_for_Shift_Right, self.D_FF2.Q, I3, S1, S0
            ),
            Clk,
            Clear_b,
        )
        return A3, A2, A1, A0


class FourBitBinaryRippleCounter:
    def __init__(self, edge: str) -> None:
        self.D_FF3, self.D_FF2, self.D_FF1, self.D_FF0 = (
            DFlipFlop(edge),
            DFlipFlop(edge),
            DFlipFlop(edge),
            DFlipFlop(edge),
        )

    def __call__(self, Count: int, Reset: int = 0) -> tuple[int, int, int, int]:
        A0, _ = self.D_FF0(self.D_FF0.Q_bar, Count, Reset)
        A1, _ = self.D_FF1(self.D_FF1.Q_bar, A0, Reset)
        A2, _ = self.D_FF2(self.D_FF2.Q_bar, A1, Reset)
        A3, _ = self.D_FF3(self.D_FF3.Q_bar, A2, Reset)
        return A3, A2, A1, A0


class BCDRippleCounter:
    def __init__(self, edge: str) -> None:
        self.JK_FF1, self.JK_FF2, self.JK_FF4, self.JK_FF8 = (
            JKFlipFlop(edge),
            JKFlipFlop(edge),
            JKFlipFlop(edge),
            JKFlipFlop(edge),
        )

    def __call__(self, Count: int, Logic: int):
        Q1 = self.JK_FF1(Logic, Logic, Count)
        Q2 = self.JK_FF2(self.JK_FF8.Q_bar, Logic, self.JK_FF1.Q)
        Q4 = self.JK_FF4(Logic, Logic, self.JK_FF2.Q)
        Q8 = self.JK_FF8(AND(self.JK_FF4.Q, self.JK_FF2.Q), Logic, self.JK_FF1.Q)
        return Q8, Q4, Q2, Q1
