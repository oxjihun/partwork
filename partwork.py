from functools import cache
from copy import deepcopy
from fractions import Fraction
import math


# 간단한 다항식 클래스
class Polynomial:
    def __init__(self, coefficient):
        self.coef = coefficient

    def __len__(self):  # 차수 반환
        return len(self.coef) - 1

    def __getitem__(self, key):
        return self.coef[key]

    def __str__(self):
        return str(self.coef)

    def __mul__(self, other):
        L = [0] * (1 + len(self) + len(other))
        for i in range(1 + len(self)):
            for j in range(1 + len(other)):
                L[i + j] += self[i] * other[j]
        return Polynomial(L)


def pol_id():
    return Polynomial([1])


def pol_unit(n):
    return Polynomial([1] + [0] * (n - 1) + [-1])


# 0부터 n까지 분할수가 담긴 리스트를 반환한다.
# 'The Theory of Partitions' Corollary 1.8 (Euler)
@cache
def p(n):
    if n == 0:
        return 1
    result = 0
    j, sgn = 1, -1
    while True:
        value = n - (j * (3 * j + sgn)) // 2
        if value >= 0:
            result -= ((-1) ** j) * p(value)
        else:
            break
        j += sgn == 1
        sgn *= -1
    return result


# 0부터 n까지 분할수 (단, part가 m개 이하)가 담긴 리스트를 반환한다.
# (1-q) * ... * (1-q^b)이라는 다항식을 먼저 계산한 후 생성함수 계수 비교
@cache
def p_with_bound(n, b):
    if n == 0:
        return 1
    pol = pol_id()
    for t in range(1, b + 1):
        pol *= pol_unit(t)
    result = 0
    for j in range(1, min(len(pol), n) + 1):
        result -= pol[j] * p_with_bound(n - j, b)
    return result


# 요주의 값
def p_rec(n, a, b):
    if a == 1:
        return p_with_bound(n, b)
    s = 0
    for i in range(n // a + 1):
        s += p_with_bound(i, b) * p_rec(n - a * i, a - 1, b)
    return s


# 생성함수를 이용하여 p_rec을 빠르게 계산하기
# 위의 p_with_bound(n) 변형
# 그런데 p_rec과 퍼포먼스가 비슷한 듯
@cache
def p_rec_gen(n, a, b):
    if n == 0:
        return 1
    pol = pol_id()
    for s in range(1, a + 1):
        for t in range(1, b + 1):
            pol *= pol_unit(s * t)
    result = 0
    for j in range(1, min(len(pol), n) + 1):
        result -= pol[j] * p_rec_gen(n - j, a, b)
    return result


# Plane Partition 위키백과의 식 구현 시도
@cache
def p_plane_boxed_gen(n, r, s, t):
    if n == 0:
        return 1
    num, den = pol_id(), pol_id()
    for i in range(1, r + 1):
        for j in range(1, s + 1):
            num *= pol_unit(i + j + t - 1)
            den *= pol_unit(i + j - 1)
    result = num[n] if len(num) >= n else 0
    for j in range(1, min(len(den), n) + 1):
        result -= den[j] * p_plane_boxed_gen(n - j, r, s, t)
    return result


# 오, 성공했다! 왜 성립하는지는 잘 모르겠지만...
# 밑에 더 좋은 식이 있었다...


def p_plane_boxed_prod(n, r, s, t):
    result = Fraction(1, 1)
    for k in range(1, t + 1):
        result *= Fraction(
            math.factorial(r + s + k - 1) * math.factorial(k - 1),
            math.factorial(r + k - 1) * math.factorial(s + k - 1),
        )
    return int(result)


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


@cache
def parts(n):
    return parts_with_bound(n, n)


def parts_rec(n, a, b):
    if a == 1:
        L = parts_with_bound(n, b)
        return [[(1, part) for part in partition] for partition in L]
    result = []
    for i in range(n // a, -1, -1):  # 큰 값부터
        L = parts_with_bound(i, b)
        R = parts_rec(n - a * i, a - 1, b)
        for l in L:
            for r in R:
                result.append(list(map(lambda p: (a, p), l)) + r)
    return result


# https://en.wikipedia.org/wiki/Plane_partition
# 아이디어: 대각선 방향으로 채우면 되지 않을까?


def diag_encode(r, s, i, j):
    assert 0 <= i < r and 0 <= j < s
    d, idx = i + j, 0
    for k in range(d):
        idx += min(k + 1, r) - max(0, k - s + 1)
    idx += i - max(0, i + j - s + 1)
    return idx


def diag_decode(r, s, idx):
    assert 0 <= idx < r * s
    NotImplemented


def diagonal_visit(r, s):
    for d in range(r + s):
        for i in range(max(0, d - s + 1), min(d + 1, r)):
            yield (i, d - i)


# 수평 수직이 더 편하다


def parts_plane_boxed(n, r, s, t):
    results = []

    def DFS(n, r, s, t, arr, i, j):
        if i == r:
            if n == 0:
                results.append(deepcopy(arr))
            return None
        for k in range(
            min(
                n,
                t,
                arr[i - 1][j] if i >= 1 else float("inf"),
                arr[i][j - 1] if j >= 1 else float("inf"),
            )
            + 1,
        ):
            arr[i][j] = k

            DFS(n - k, r, s, t, arr, i + (j == s - 1), (j + 1) % s)
        arr[i][j] = 0

    DFS(n, r, s, t, [[0] * s for _ in range(r)], 0, 0)
    return results


def parts_plane_boxed_tall(n, r, s):  # 높이 제한 x
    return parts_plane_boxed(n, r, s, n)


def parts_rec_encoded(n, r, s):
    def check_submatrix(arr):
        for i in range(len(arr) - 1):
            for j in range(len(arr[0]) - 1):
                if arr[i][j] + arr[i + 1][j + 1] < arr[i + 1][j] + arr[i][j + 1]:
                    return False
        return True

    return list(filter(check_submatrix, parts_plane_boxed_tall(n, r, s)))


# 2023-09-11
def overlap(R, a, b):
    M = [[0] * b for _ in range(a)]
    for x, y in R:
        for i in range(x):
            for j in range(y):
                M[i][j] += 1
    return M


def delta(M):
    a, b = len(M), len(M[0])
    dM = [[0] * b for _ in range(a)]
    for i in range(a):
        for j in range(b):
            dM[i][j] = M[i][j]
            if i < a - 1:
                dM[i][j] -= M[i + 1][j]
            if j < b - 1:
                dM[i][j] -= M[i][j + 1]
            if (i < a - 1) and (j < b - 1):
                dM[i][j] += M[i + 1][j + 1]
    return dM


def separate(M):
    a, b = len(M), len(M[0])
    dM = delta(M)
    R = []
    for i in range(a):
        for j in range(b):
            for _ in range(dM[i][j]):
                R.append((i, j))
    return R, a, b


def to_tuple(M):
    return tuple(tuple(_) for _ in M)


def format2x2(M):
    assert len(M) == len(M[0]) == 2
    return "%s %s\n" * 2 % tuple(M[0] + M[1])


def format2x3(M):
    assert len(M) == 2 and len(M[0]) == 3
    return "%s %s %s\n" * 2 % tuple(M[0] + M[1])
