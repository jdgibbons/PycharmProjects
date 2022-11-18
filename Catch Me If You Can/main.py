# This is a sample Python script.

def read_file_to_list(filename):
    contents = []
    my_file = open(filename)
    for line in my_file:
        contents.append(line.strip())

    my_file.close()
    return contents


def import_usable_faces(filename):
    with open(filename, 'r') as my_file:
        contents = my_file.readlines()
    return contents


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    lines = read_file_to_list('usable9000quotes.csv')
    linear = import_usable_faces('usable9000quotes.csv')
    print('Finished.')

print('End of line.')
