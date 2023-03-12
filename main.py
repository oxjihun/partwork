# 0부터 n까지 number of partitions 반환 3월 12일에 작성함 12쪽 Euler의 Corollary 이용
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


# parts 수가 m개 이하 (혹은 각 parts가 m이하) / 위에 오일러 아이디어, 생성함수의 역 보고 생각. 이것도 3월 12일 작성
def list_p_with_bound(n, m):
    # build polynomial (1-q) * ... * (1-q^m)
    pol = [1] + [0] * ((m * (m + 1)) // 2)
    for t in range(1, m + 1):
        for s in range((t * (t - 1)) // 2, -1, -1):
            pol[t + s] -= pol[s]
    # compute
    memo = [0] * (n + 1)
    memo[0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(len(pol), i + 1)):
            memo[i] -= pol[j] * memo[i - j]
    return memo


lookup_table = [None] + [list_p_with_bound(1000, m) for m in range(1, 11)]  # 이 테이블의 m열이


def objective(n, a, b):
    if a == 1:
        return lookup_table[b][n]
    s = 0
    for i in range(min(n // a, b) + 1):
        s += lookup_table[b][i] * objective(n - a * i, a - 1, b)
    return s


a = 1
for b in range(1, 11):
    print(objective(a * b, a, b))  # 예상한 결과

a = 2
for b in range(1, 11):
    print(objective(a * b, a, b))  # OEIS에 없다

a = 3
for b in range(1, 11):
    print(objective(a * b, a, b))  # OEIS에 없다

a = 4
for b in range(1, 11):
    print(objective(a * b, a, b))  # OEIS에 없다 어 잠깐 왜 시작값이 4지

print(objective(4, 1, 4))
print(objective(4, 4, 1))
