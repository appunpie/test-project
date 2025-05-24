from collections import Counter

def find_duplicates(nums):
    freq = Counter(nums)
    ans = [num for num, count in freq.items() if count >= 2]
    return sorted(ans)

def main():
    import sys
    nums = list(map(int, sys.stdin.readline().split()))
    result = find_duplicates(nums)
    print(result)

if __name__ == "__main__":
    main()