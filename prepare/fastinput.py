import sys

# Fast input
input = sys.stdin.readline

# Read comma-separated numbers
nums = list(map(float, input().strip().split(',')))

# Print with 2 decimal places
for x in nums:
    print(f"{x:.2f}")