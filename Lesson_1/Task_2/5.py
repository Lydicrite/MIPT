import random

N = 25
vector = [random.randint(-100, 100) for _ in range(N)]
print(vector)

source = vector.copy()

for i in range(N):
    if source[i] < 0:
        left = None
        right = None

        for l in range(i - 1, -1, -1):
            if source[l] > 0:
                left = source[l]
                break

        for r in range(i + 1, N):
            if source[r] > 0:
                right = source[r]
                break

        if left is not None and right is not None:
            vector[i] = (left + right) / 2
        elif left is not None:
            vector[i] = left
        elif right is not None:
            vector[i] = right

print(vector)
