import partwork


# 값 출력 (Technical)

import math

N = 10
p_rec_table = [[None] * (N + 1) for _ in range(N + 1)]
for a in range(1, N + 1):
    for b in range(1, N + 1):
        p_rec_table[a][b] = partwork.p_rec(a * b, a, b)
        """int(
            (
                math.log(
                    4 * math.sqrt(3) * (a * b) * p_rec(a * b, a, b)
                )  # a+b는 왠지 아닌 것 같다
                / (math.pi * math.sqrt(2 / 3))
            )
            ** 2
            / ((a * b) / 1000)
        )
        """
for a in range(1, N + 1):
    print(
        " ".join(
            [
                ("{:%dd}" % (len(str(p_rec_table[-1][b])))).format(p_rec_table[a][b])
                for b in range(1, N + 1)
            ]
        )
    )
