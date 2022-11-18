flatter = []


def flatten_my_lists(data):
    for element in data:
        if type(element) == list:
            flatten_my_lists(element)
        else:
            flatter.append(element)


def flatten(L):
    for item in L:
        try:
            yield from flatten(item)
        except TypeError:
            yield item

listy = [[[[1, 16], 31], 46], 61]
# flatten_my_lists(listy)
#
# print(flatter)

print("Without a global")

ynot = list(flatten(listy))

print(ynot)


