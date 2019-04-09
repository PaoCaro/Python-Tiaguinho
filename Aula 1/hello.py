def print_average(num_list):
    print(average(num_list))

def average(num_list):
    num = len(num_list)
    total = sum(num_list)
    if num != 0:
        media = total / num
    else:
        return 0

print_average([1, 2, 3, 4, 5, 6,])