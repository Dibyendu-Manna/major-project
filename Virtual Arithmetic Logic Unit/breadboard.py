# from util.synthesis import canonical

# def truth_table(sop: str):
#     products = sop.replace(" ", "").split("+")
#     inputs = list({character for character in sop if character.isalpha()})
#     inputs.sort()
#     return products


# def hamming_distance(A: str, B: str):
#     """
#     Calculate the Hamming distance between two binary strings.
#     """
#     dif = 0
#     for a, b in zip(A, B):
#         if a not in ("0", "1") or b not in ("0", "1"):
#             raise ValueError("Inputs must be binary strings ('0' or '1').")
#         if a != b:
#             dif += 1
#     return dif


# # print(
# #     minterm(


# #     )
# # )

# """
# {'function': 'F',
# 'minterms': {0: '000', 2: '010', 4: '100', 7: '111'},
# 'maxterms': {1: '001', 5: '101', 6: '110'},
# "don't cares": {3: '011'},
# 'm': '∑ m(0,2,4,7)',
# 'M': '∏ M(1,5,6)',
# 'd': 'd(3)',
# 'sop': 'F(x,y,z) = x′y′z′ + x′yz′ + xy′z′ + xyz',
# 'pos': 'F(x,y,z) = (x + y + z′) (x′ + y + z′) (x′ + y′ + z)'},
# """


# def tabular(truth_table: str):
#     """ """
#     from collections import defaultdict

#     def group(m: list[str]) -> dict[int, list[str]]:
#         grp: defaultdict[int, list[str]] = defaultdict(list)
#         for minterm in m:
#             grp[minterm.count("1")].append(minterm)
#         return dict(grp)

#     def combine(minterm_1: str, minterm_2: str):
#         cmb = []
#         for m_1, m_2 in zip(minterm_1, minterm_2):
#             if m_1 != m_2:
#                 cmb.append("-")
#             else:
#                 cmb.append(m_1)

#     canonicals = canonical(truth_table)
#     minterms = [
#         list(c["minterms"].values()) + list(c["don't cares"].values())
#         for c in canonicals
#     ]
#     step1 = [group(minterm) for minterm in minterms]
#     # step2 = []
#     # for gr in step1:
#     #     for g in gr.keys():
#     #         ...

#     return step1


# tabular(
#     """
# x y z | F G
# 0 0 0 | 1 0
# 0 0 1 | 0 1
# 0 1 0 | 1 x
# 0 1 1 | x 1
# 1 0 0 | 1 0
# 1 0 1 | 0 1
# 1 1 0 | 0 x
# 1 1 1 | 1 0
# """
# )
