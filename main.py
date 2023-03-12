# 0부터 n까지 number of partitions 반환 3월 12일에 작성함 12쪽 Euler의 Corollary 이용
def plist(n):
    memo = [0] * (n + 1)
    memo[0] = 1
    for i in range(1, n + 1):
        for j in range(1, int((2 * n / 3) ** 0.5) + 2):
            temp = i - (j * (3 * j - 1)) // 2
            if temp >= 0:
                memo[i] -= ((-1) ** j) * memo[temp]
            temp = i - (j * (3 * j + 1)) // 2
            if temp >= 0:
                memo[i] -= ((-1) ** j) * memo[temp]
    return memo


# parts 수가 m개 이하 (혹은 각 parts가 m이하) / 위에 오일러 아이디어, 생성함수의 역 보고 생각. 이것도 3월 12일 작성
def plist_bound(n, m):
    # build polynomial (1-q) * ... * (1-q^m)
    pol = [0] * (1 + (m * (m + 1)) // 2)
    pol[0] = 1
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


glist = plist(1000)  # 글로벌 참조용


def objective(n, a, b):
    if n > a * b:
        return 0
    if a == 1:
        return glist[n]
    s = 0
    for i in range(1, b + 1):
        s += glist[i] * objective(n - a * i, a - 1, b)
    return s


L = plist_bound(20, 3)
print(L, len(L))

print(objective(0, 2, 3))
