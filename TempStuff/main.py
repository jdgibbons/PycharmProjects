class Animal():
    def __init__(self):
        print("ANIMAL CREATED!")

    def who_am_i(self):
        print("I am an animal.")

    def speak(self):
        print("Generic animal noise.")


class Dog(Animal):
    def __init__(self):
        Animal.__init__(self)
        print("Dog created!")

    def who_am_i(self):
        print("I am a dog.")

    def speak(self):
        print("Woof!!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Thanks for playing!')
    dog = Dog()
    dog.speak()