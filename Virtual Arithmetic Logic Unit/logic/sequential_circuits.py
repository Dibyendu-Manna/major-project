from .logicgates import AND, OR, NOT, NAND, NOR, XOR


__all__ = [
    "SRLatch",
    "SNotRNotLatch",
    "SREnLatch",
    "DLatch",
    "DFlipFlop",
    "JKFlipFlop",
    "TFlipFlop",
]


class SRLatch:
    """ """

    def __init__(self) -> None:
        self.R, self.S = 0, 0
        self.Q, self.Q_bar = 0, 1
        self.Q, self.Q_bar = self(self.S, self.R)

    def __str__(self) -> str:
        return (
            "    ┌─────────┐\n"
            "    │         │\n"
            f"{self.S} ──┤S       Q├── {self.Q}\n"
            "    │         │\n"
            "    │         │\n"
            "    │         │\n"
            f"{self.R} ──┤R      Q′├○─ {self.Q_bar}\n"
            "    │         │\n"
            "    └─────────┘\n"
        )

    def __call__(self, S: int, R: int) -> tuple[int, int]:
        if R != self.R:
            self.Q = NOR(R, self.Q_bar)
            self.Q_bar = NOR(self.Q, S)
        if S != self.S:
            self.Q_bar = NOR(S, self.Q)
            self.Q = NOR(self.Q_bar, R)
        self.S, self.R = S, R
        return self.Q, self.Q_bar


class SNotRNotLatch:
    """ """

    def __init__(self) -> None:
        self.S_not, self.R_not = 1, 1
        self.Q, self.Q_bar = 0, 1
        self.Q, self.Q_bar = self(self.S_not, self.R_not)

    def __str__(self) -> str:
        return (
            "    ┌─────────┐\n"
            "    │         │\n"
            f"{self.S_not} ─○┤S       Q├── {self.Q}\n"
            "    │         │\n"
            "    │         │\n"
            "    │         │\n"
            f"{self.R_not} ─○┤R      Q′├○─ {self.Q_bar}\n"
            "    │         │\n"
            "    └─────────┘\n"
        )

    def __call__(self, S_not: int, R_not: int) -> tuple[int, int]:
        if S_not != self.S_not:
            self.Q = NAND(S_not, self.Q_bar)
            self.Q_bar = NAND(self.Q, R_not)
        if R_not != self.R_not:
            self.Q_bar = NAND(R_not, self.Q)
            self.Q = NAND(self.Q_bar, S_not)
        self.S_not, self.R_not = S_not, R_not
        return self.Q, self.Q_bar


class SREnLatch:
    """ """

    def __init__(self) -> None:
        self.S, self.R, self.En = 0, 0, 1
        self.Q, self.Q_bar = 0, 1
        self.Q, self.Q_bar = self(self.S, self.R, self.En)

    def __str__(self) -> str:
        return (
            "    ┌─────────┐\n"
            "    │         │\n"
            f"{self.S} ──┤S       Q├── {self.Q}\n"
            "    │         │\n"
            f"{self.En} ──┤En       │\n"
            "    │         │\n"
            f"{self.R} ──┤R      Q′├○─ {self.Q_bar}\n"
            "    │         │\n"
            "    └─────────┘\n"
        )

    def __call__(self, S: int, R: int, En: int = 1) -> tuple[int, int]:
        if S != self.S:
            self.Q = NAND(NAND(S, En), self.Q_bar)
            self.Q_bar = NAND(self.Q, NAND(En, R))
        if R != self.R:
            self.Q_bar = NAND(NAND(En, R), self.Q)
            self.Q = NAND(self.Q_bar, NAND(S, En))
        self.S, self.R, self.En = S, R, En
        return self.Q, self.Q_bar


class DLatch:
    """ """

    def __init__(self) -> None:
        self.D, self.En, self.Set, self.Reset = 0, 0, 1, 1
        self.Q, self.Q_bar = 0, 1
        self.Q, self.Q_bar = self(self.D, self.En, self.Reset, self.Set)

    def __str__(self) -> str:
        return (
            f"{self.Set} ───────┐\n"
            "    ┌────○────┐\n"
            "    │    S    │\n"
            f"{self.D} ──┤D       Q├── {self.Q}\n"
            "    │         │\n"
            "    │         │\n"
            "    │         │\n"
            f"{self.En} ──┤En     Q′├○─ {self.Q_bar}\n"
            "    │    R    │\n"
            "    └────○────┘\n"
            f"{self.Reset} ───────┘\n"
        )

    def __call__(
        self, D: int, En: int, Reset: int = 1, Set: int = 1
    ) -> tuple[int, int]:
        for _ in range(2):
            self.Q = NAND(Set, NAND(D, En), self.Q_bar)
            self.Q_bar = NAND(self.Q, NAND(En, NOT(D)), Reset)
        self.D, self.En, self.Reset, self.Set = D, En, Reset, Set
        return self.Q, self.Q_bar


class DFlipFlop:
    """ """

    def __init__(self, type: str) -> None:
        self.type = type
        self.D, self.Clk, self.Reset, self.Set = 0, 0, 1, 1
        if self.type == "p":
            self.__S, self.__R, self.__X2 = 1, 1, 1
            self.Q_bar = 1
            for _ in range(2):
                self.__X1 = NAND(self.Set, self.__X2, self.__S)
                self.__S = NAND(self.__X1, self.Clk, self.Reset)
            for _ in range(2):
                self.__R = NAND(self.Set, self.__S, self.Clk, self.__X2)
                self.__X2 = NAND(self.__R, self.D, self.Reset)
            for _ in range(2):
                self.Q = NAND(self.Set, self.__S, self.Q_bar)
                self.Q_bar = NAND(self.Q, self.__R, self.Reset)
        elif self.type == "n":
            self.__master, self.__slave = DLatch(), DLatch()
            self.__Y, self.Q_bar = self.__master(self.D, self.Clk, self.Reset, self.Set)
            self.Q, self.Q_bar = self.__slave(
                self.__Y, NOT(self.Clk), self.Reset, self.Set
            )
        else:
            raise ValueError(
                "Flip-Flop must only be Positive-edge-triggered ('p' type) or Negative-edge-triggered ('n' type)."
            )

    def __str__(self) -> str:
        return (
            f"{self.Set} ───────┐\n"
            "    ┌────○────┐\n"
            "    │    S    │\n"
            f"{self.D} ──┤D       Q├── {self.Q}\n"
            "    │         │\n"
            "    │         │\n"
            f"{self.Clk} ─{'─' if (self.type == 'p') else '○'}┤▷ Clk    │\n"
            f"    │       Q′├○─ {self.Q_bar}\n"
            "    │    R    │\n"
            "    └────○────┘\n"
            f"{self.Reset} ───────┘\n"
        )

    def __call__(
        self, D: int, Clk: int, Reset: int = 1, Set: int = 1
    ) -> tuple[int, int]:
        if self.type == "p":
            for _ in range(2):
                self.__X1 = NAND(Set, self.__X2, self.__S)
                self.__S = NAND(self.__X1, Clk, Reset)
            for _ in range(2):
                self.__R = NAND(Set, self.__S, Clk, self.__X2)
                self.__X2 = NAND(self.__R, D, Reset)
            for _ in range(2):
                self.Q = NAND(Set, self.__S, self.Q_bar)
                self.Q_bar = NAND(self.Q, self.__R, Reset)
        elif self.type == "n":
            self.__Y, self.Q_bar = self.__master(D, Clk, Reset, Set)
            self.Q, self.Q_bar = self.__slave(self.__Y, NOT(Clk), Reset, Set)
        self.D, self.Clk, self.Reset, self.Set = D, Clk, Set, Reset
        return self.Q, self.Q_bar


class JKFlipFlop:
    def __init__(self, type: str) -> None:
        self.type = type
        self.J, self.K, self.Clk = 0, 0, 0
        self.__d_flipflop = DFlipFlop(self.type)
        self.Q, self.Q_bar = self(self.J, self.K, self.Clk)

    def __str__(self) -> str:
        return (
            "    ┌─────────┐\n"
            "    │         │\n"
            f"{self.J} ──┤J       Q├── {self.Q}\n"
            "    │         │\n"
            f"{self.Clk} ─{'─' if (self.type == 'p') else '○'}┤▷ Clk    │\n"
            "    │         │\n"
            f"{self.K} ──┤K      Q′├○─ {self.Q_bar}\n"
            "    │         │\n"
            "    └─────────┘\n"
        )

    def __call__(self, J: int, K: int, Clk: int) -> tuple[int, int]:
        self.Q, self.Q_bar = self.__d_flipflop(
            OR(AND(self.__d_flipflop.Q_bar, J), AND(NOT(K), self.__d_flipflop.Q)),
            Clk,
        )
        self.J, self.K, self.Clk = J, K, Clk
        return self.Q, self.Q_bar


class TFlipFlop:
    """ """

    def __init__(self, type: str) -> None:
        self.type = type
        self.T, self.Clk = 0, 0
        self.__d_flipflop = DFlipFlop(self.type)
        self.Q, self.Q_bar = self(self.T, self.Clk)

    def __str__(self) -> str:
        return (
            "    ┌─────────┐\n"
            "    │         │\n"
            f"{self.T} ──┤T       Q├── {self.Q}\n"
            "    │         │\n"
            "    │         │\n"
            "    │         │\n"
            f"{self.Clk} ─{'─' if (self.type == 'p') else '○'}┤▷ Clk  Q′├○─ {self.Q_bar}\n"
            "    │         │\n"
            "    └─────────┘\n"
        )

    def __call__(self, T: int, Clk: int) -> tuple[int, int]:
        self.Q, self.Q_bar = self.__d_flipflop(XOR(self.__d_flipflop.Q, T), Clk)
        self.T, self.Clk = T, Clk
        return self.Q, self.Q_bar
