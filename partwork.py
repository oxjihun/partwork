# https://www.daleseo.com/python-cache/
from functools import cache


# 0부터 n까지 분할수가 담긴 리스트를 반환한다.
# 'The Theory of Partitions' Corollary 1.8 (Euler)
@cache
def p(n):
    if n == 0:
        return 1
    ans = 0
    j, sgn = 1, -1
    while True:
        value = n - (j * (3 * j + sgn)) // 2
        if value >= 0:
            ans -= ((-1) ** j) * p(value)
        else:
            break
        j += sgn == 1
        sgn *= -1
    return ans


# 0부터 n까지 분할수 (단, part가 m개 이하)가 담긴 리스트를 반환한다.
# (1-q) * ... * (1-q^m)이라는 다항식을 먼저 계산한 후 생성함수 계수 비교
memo_p_with_bound = [None]


def p_with_bound(n, b):
    for _ in range(len(memo_p_with_bound), b + 1):
        memo_p_with_bound.append([1])
    if n <= len(memo_p_with_bound[b]) - 1:
        return memo_p_with_bound[b][n]
    pol = [1] + [0] * ((b * (b + 1)) // 2)
    for t in range(1, b + 1):
        for s in range((t * (t - 1)) // 2, -1, -1):
            pol[t + s] -= pol[s]
    for i in range(1, n + 1):
        for j in range(1, min(len(pol), i + 1)):
            memo_p_with_bound[b].append(0)
            memo_p_with_bound[b][i] -= pol[j] * memo_p_with_bound[b][i - j]
    return memo_p_with_bound[b][n]


# 요주의 값
def p_rec(n, a, b):
    if a == 1:
        return p_with_bound(n, b)
    s = 0
    for i in range(n // a + 1):
        s += p_with_bound(i, b) * p_rec(n - a * i, a - 1, b)
    return s


# 값 출력 (Technical)

import math

N = 10
p_rec_table = [[None] * (N + 1) for _ in range(N + 1)]
for a in range(1, N + 1):
    for b in range(1, N + 1):
        p_rec_table[a][b] = p_rec(a * b, a, b)
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

# 3월 13일


def parts_with_bound(n, b):
    if n == 0:
        return [[]]  # 중요
    if b == 1:  # 모든 조각이 1
        return [[1] * n]
    result = []
    for i in range(min(n, b), 0, -1):  # 가장 큰 조각이 min(n, b)일 때부터 1일 때까지
        for j in range(n // i, 0, -1):  # 그 조각은 1번부터 n//i번까지 나타날 수 있음
            # print(n - i * j, i - 1)
            L = parts_with_bound(n - i * j, i - 1)
            for partition in L:
                result.append([i] * j + partition)
    return result


def parts(n):
    return parts_with_bound(n, n)


def p_rec_parts(n, a, b):
    if a == 1:
        L = parts_with_bound(n, b)
        return [[(1, part) for part in partition] for partition in L]
    result = []
    for i in range(n // a, -1, -1):  # 큰 값부터
        L = parts_with_bound(i, b)
        R = p_rec_parts(n - a * i, a - 1, b)
        for l in L:
            for r in R:
                result.append(list(map(lambda p: (a, p), l)) + r)
    return result


# print(parts(5))
for _ in p_rec_parts(9, 3, 3):
    print(_)


def check_asym_with_desmos(n):
    return list(enumerate(list_p(n)))


# print(*check_asym_with_desmos(100))
# \frac{1}{4x\sqrt{3}}e^{\pi\sqrt{\frac{2}{3}x}} desmos로 그려보니 잘 맞는다
