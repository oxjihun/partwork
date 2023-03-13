# 0부터 n까지 분할수가 담긴 리스트를 반환한다.
# 'The Theory of Partitions' Corollary 1.8 (Euler)
def list_p(n):
    memo = [1] + [0] * n
    for i in range(1, n + 1):
        j, sgn = 1, -1
        while True:
            value = i - (j * (3 * j + sgn)) // 2
            if value >= 0:
                memo[i] -= ((-1) ** j) * memo[value]
            else:
                break
            j += sgn == 1
            sgn *= -1
    return memo


# 0부터 n까지 분할수 (단, part가 m개 이하)가 담긴 리스트를 반환한다.
# (1-q) * ... * (1-q^m)이라는 다항식을 먼저 계산한 후 생성함수 계수 비교
def list_p_with_bound(n, m):
    pol = [1] + [0] * ((m * (m + 1)) // 2)
    for t in range(1, m + 1):
        for s in range((t * (t - 1)) // 2, -1, -1):
            pol[t + s] -= pol[s]
    memo = [0] * (n + 1)
    memo[0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(len(pol), i + 1)):
            memo[i] -= pol[j] * memo[i - j]
    return memo


lookup_table = [None] + [list_p_with_bound(1000, m) for m in range(1, 31)]  # 참조용 리스트
print("Built lookup table.")


# 요주의 값
def objective(n, a, b):
    if a == 1:
        return lookup_table[b][n]
    s = 0
    for i in range(n // a + 1):
        s += lookup_table[b][i] * objective(n - a * i, a - 1, b)
    return s


# 값 출력 (Technical)
N = 10
objective_table = [[None] * (N + 1) for _ in range(N + 1)]
for a in range(1, N + 1):
    for b in range(1, N + 1):
        objective_table[a][b] = objective(a * b, a, b)
for a in range(1, N + 1):
    print(
        " ".join(
            [
                ("{:%dd}" % (len(str(objective_table[-1][b])))).format(
                    objective_table[a][b]
                )
                for b in range(1, N + 1)
            ]
        )
    )
