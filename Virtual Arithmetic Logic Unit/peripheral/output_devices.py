def seven_segment_displays(*segments: tuple[int, int, int, int, int, int, int]) -> None:
    """ """
    # *      ╷  ────┐  ────┐ ╷    ╷ ┌────  ┌────   ────┐ ┌────┐ ┌────┐ ┌────┐  * Top
    # *      │      │      │ │    │ │      │           │ │    │ │    │ │    │  * Upper Middle
    # *      │ ┌────┘  ────┤ └────┤ └────┐ ├────┐      │ ├────┤ └────┤ │    │  * Middle
    # *      │ │           │      │      │ │    │      │ │    │      │ │    │  * Lower Middle
    # *      ╵ └────   ────┘      ╵  ────┘ └────┘      ╵ └────┘  ────┘ └────┘  * Bottom

    top = []
    upper_middle = []
    middle = []
    lower_middle = []
    bottom = []

    for segment in segments:
        if any(bit not in (0, 1) for bit in segment):
            raise ValueError("Inputs must be binary (0 or 1).")
        a, b, c, d, e, f, g = segment
        top.append(
            f"{'┌' if (f and a) else '╷' if f else ' '}{'────' if a else '    '}{'┐' if (a and b) else '╷' if b else ' '} "
        )
        upper_middle.append(f"{'│' if f else ' '}    {'│' if b else ' '} ")
        middle.append(
            f"{'├' if (e and f and g) else '┌' if (e and g) else '└' if (g and f) else '│' if (e and f) else ' '}{'────' if g else '    '}{'┤' if (b and c and g) else '┘' if (b and g) else '┐' if (g and c) else '│' if (b and c) else ' '} "
        )
        lower_middle.append(f"{'│' if e else ' '}    {'│' if c else ' '} ")
        bottom.append(
            f"{'└' if (d and e) else '╵' if e else ' '}{'────' if d else '    '}{'┘' if (c and d) else '╵' if c else ' '} "
        )

    print("".join(top))
    print("".join(upper_middle))
    print("".join(middle))
    print("".join(lower_middle))
    print("".join(bottom))
