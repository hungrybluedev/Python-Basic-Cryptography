from bisect import bisect_left


def binary_search(arr, key, lower=0, upper=None):
    upper = upper or len(arr)
    # bisect_left returns the position where key should be inserted
    # provided that the list is in
    position = bisect_left(arr, key, lower, upper)
    return position if position != upper and arr[position] == key else -1
