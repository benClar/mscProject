import sys
import Line_read
"""Returns out interquartile range for input values"""

def get_inter_quartile(nums):
    result = {}
    nums.sort()
    total = len(nums)
    result['lower_q'] = nums[int((total + 1) / 4)]
    result['upper_q'] = nums[int((3 * (total + 1)) / 4)]
    result['low_whisker'] = nums[0]
    result['high_whisker'] = result['upper_q'] + ((result['upper_q'] - result['lower_q']) * 1.5)
    result['median'] = nums[int((total + 1) / 2)]
    result['mean'] = get_mean(nums)
    return result

def get_mean(nums):
    result = 0
    for i in nums:
        result += i
    return (result / len(nums))


if __name__ == '__main__':
    inter_range_q = get_inter_quartile(Line_read.read(sys.argv[1]))
    for key, value in inter_range_q.items():
        print(key, value)