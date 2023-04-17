from functools import cache


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
    pol = Polynomial([1])
    for t in range(1, b + 1):
        pol *= Polynomial([1] + [0] * (t - 1) + [-1])
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
