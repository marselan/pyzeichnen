import random
import sys

def array_is_in_order(arr):
    for i in range(0, len(arr)-1):
        if arr[i] > arr[i+1]:
            return False
    return True

def array_is_balanced(arr, pivot_index):
    if pivot_index < 0:
        return True
    for i in range(0, pivot_index):
        if arr[pivot_index] < arr[i]:
            return False
    for i in range(pivot_index + 1, len(arr)):
        if arr[i] < arr[pivot_index]:
            return False
    return True

def partition(arr, low, high):
    if high < low:
        return -1
    pivot = arr[high]
    current_index = low - 1
    for i in range(low, high):
        if arr[i] <= pivot:
            current_index += 1
            arr[i], arr[current_index] = arr[current_index], arr[i]
    current_index += 1
    arr[current_index], arr[high] = pivot, arr[current_index]
    return current_index

def quick_sort_partition(arr, low, high):
    if high <= low:
        return
    pivot = partition(arr, low, high)
    quick_sort_partition(arr, low, pivot-1)
    quick_sort_partition(arr, pivot+1, high)

def quick_sort(arr):
    quick_sort_partition(arr, 0, len(arr)-1)


if __name__ == '__main__':
    arr = random.sample(range(0, 100000), 10000)
    quick_sort(arr)
    print(array_is_in_order(arr))
