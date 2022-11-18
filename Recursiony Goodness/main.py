# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def fibonacci(nthNumber):
    print(f"fibonacci({nthNumber}) called.")
    if nthNumber == 1 or nthNumber == 2:
        # Base Case
        print(f"Call to fibonacci({nthNumber}) returning 1.")
        return 1
    else:
        # Recursive Case
        print(f"Calling fibonacci({nthNumber - 1}) and fibonacci({nthNumber - 2}).")
        # result1 = fibonacci(nthNumber - 1)
        # result2 = fibonacci(nthNumber - 2)
        # result3 = result1 + result2
        result = fibonacci(nthNumber - 1) + fibonacci(nthNumber - 2)
        print(f"Call to fibonacci({nthNumber}) returning as {result}.")
        return result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(fibonacci(10))
