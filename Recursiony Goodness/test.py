def isPalindrome(theString):
    if len(theString) == 0 or len(theString) == 1:
        # Base Case
        return True
    else:
        # Recursive Case
        head = theString[0]
        middle = theString[1:-1]
        last = theString[-1]
        return head == last and isPalindrome(middle)

text = 'racecar'
print(text + ' is a palindrome: ' + str(isPalindrome(text)))
text = 'amanaplanacanalpanama'
print(text + ' is a palindrome: ' + str(isPalindrome(text)))
text = 'tacocat'
print(text + ' is a palindrome: ' + str(isPalindrome(text)))
text = 'zophie'
print(text + ' is a palindrome: ' + str(isPalindrome(text)))
