A = [1, 4, 3, 7, 6, 8, 5, 9]
F = [1, -2, 1]

B = []
for i in range(len(A) - len(F) + 1):
    s = 0
    for j in range(len(F)):
        s += A[i + j] * F[j]
    B.append(s)

print(A)
print(F)
print(B)