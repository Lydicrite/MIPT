import random

SAMPLE_SIZE = 20
nums = [random.randint(0, 100) for _ in range(SAMPLE_SIZE)]
print(nums)

gist = [0] * 10
for num in nums:
    gist[num // 10] += 1
print(gist)

prob = [count / SAMPLE_SIZE for count in gist]
print(prob)
