import itertools
import numpy

listing = [[1, 2],
           [16, 17],
           [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45],
           [46, 47],
           [61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]]

listing2 = [1, 16, 31, 46, 61]
listing3 = [2, 17, 32, 47, 62]

train = numpy.matrix([listing2, listing3]).transpose().tolist()

train[2] = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]

training = list(itertools.product(*train))
print(train)
for t in training:
    print(t)
print(len(training))

# print(list(itertools.product(*listing)))
#
# a = list(itertools.product(*listing))
# for what in a:
#     print(what)
#
# cc = [2, 16, 41, 47, 63]
#
# dd = tuple(cc)
#
# if tuple(cc) in a:
#     print("Yes, I see it's in here.")
# else:
#     print("Nope, not seeing it.")
#
# print('Whatevers')
