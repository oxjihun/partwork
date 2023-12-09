# 2023-12-10 오전 3시 30분 검수 끝

import partwork, math, pyperclip


def gen_desmos(start, end, a, b):  # Desmos 입력용 데이터 생성
    L = []
    for n in range(start, end + 1):
        # print(n, a, b)
        p_p = partwork.p_plane_boxed_gen(n, a, b, n)
        p_rec = partwork.p_rec_gen(n, a, b)
        L.append(f"({n},{p_rec/p_p})")
    text = ",".join(L)
    print(text)
    pyperclip.copy(text)


def gen_compare_2x3(n):  # 2x3 평면 분할을 Good와 Bad로 분류
    M = set(map(partwork.to_tuple, partwork.parts_rec_encoded(n, 2, 3)))
    P_p = set(map(partwork.to_tuple, partwork.parts_plane_boxed_tall(n, 2, 3)))

    with open("results/Good Matrices (2x3) (n = %s).txt" % n, "w") as file:
        for _ in M:
            file.write(partwork.format2x3(_) + "\n")

    with open("results/Bad Matrices (2x3) (n = %s).txt" % n, "w") as file:
        for _ in P_p - M:
            file.write(partwork.format2x3(_) + "\n")


# 결국 numpy는 쓰지 않았다. from numpy.polynomial import Polynomial
