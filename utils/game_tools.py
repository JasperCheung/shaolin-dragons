import random


# Given a word, return a list of random letters including all the
# letters from the word
def random_letter_list(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    lst = list()
    for char in word:
        lst.append(char)
    while len(lst) < 16:
        lst.append(random.choice(letters))
    random.shuffle(lst)
    return lst

if __name__ == "__main__":
    print random_letter_list("kitten")
    print random_letter_list("apple")
    print random_letter_list("pyramid")
    print random_letter_list("arithmetic")
