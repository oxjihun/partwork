# polytope 공식 예제 참고함
# 9월 25일 1교시에 작성중

import polytope as pc
import numpy as np

a, b = 2, 3
m = a * b


def change_var(L, i, j, delta):
    if i == (a - 1) and j == (b - 1):
        for _ in range(m - 1):
            L[_] -= delta
        return -delta
    L[i * b + j] += delta
    return 0


A, vb = [], []
# 각 변수가 0에서 1 사이
for i in range(a):
    for j in range(b):
        A.append([0] * (m - 1))
        vb.append(1 + change_var(A[-1], i, j, 1))
        A.append([0] * (m - 1))
        vb.append(0 + change_var(A[-1], i, j, -1))
# 그냥 plane partition
A_bad, vb_bad = A[:], vb[:]
for i in range(a):
    for j in range(b):
        if i < a - 1:
            A_bad.append([0] * (m - 1))
            vb_bad.append(
                change_var(A_bad[-1], i, j, -1) + change_var(A_bad[-1], i + 1, j, 1)
            )
        if j < b - 1:
            A_bad.append([0] * (m - 1))
            vb_bad.append(
                change_var(A_bad[-1], i, j, -1) + change_var(A_bad[-1], i, j + 1, 1)
            )
# Good matrix
A_good, vb_good = A[:], vb[:]
for i in range(a):
    for j in range(b):
        A_good.append([0] * (m - 1))
        vb_good.append(change_var(A_good[-1], i, j, -1))
        if i < a - 1:
            vb_good[-1] += change_var(A_good[-1], i + 1, j, 1)
        if j < b - 1:
            vb_good[-1] += change_var(A_good[-1], i, j + 1, 1)
        if i < a - 1 and j < b - 1:
            vb_good[-1] += change_var(A_good[-1], i + 1, j + 1, -1)

p_bad = pc.Polytope(np.array(A_bad), np.array(vb_bad))
p_good = pc.Polytope(np.array(A_good), np.array(vb_good))

print(f"{p_good.volume} / {p_bad.volume} = {p_good.volume/p_bad.volume}")
