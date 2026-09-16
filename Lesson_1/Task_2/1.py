import random

SAMPLE_SIZE = 7
nums = [random.uniform(-17, 17) for _ in range(SAMPLE_SIZE)]
print(nums)

nums.sort()
print(f"Минимальное значение: {nums[0]}")
print(f"Максимальное значение: {nums[-1]}")
print(f"Медиана: { nums[len(nums) // 2] if len(nums) % 2 != 0 else (nums[len(nums) // 2 - 1] + nums[len(nums) // 2]) / 2 }.")
