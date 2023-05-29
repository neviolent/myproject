import random
from colorama import init, Fore

def find_common_letters(common_letters_list, word):
    result = []
    for letter in word:
        if letter in common_letters_list:
            result.append(letter)
    return result

def check_letters_in_word(word_a, word_b):
    letters_list = []
    for letter in word_a:
        if letter in word_b and letter not in letters_list:
            letters_list.append(letter)
    return letters_list

init(autoreset=True)
words = ("лодка","князь","адепт","ангел","земля","грязь","червь","зверь","канун","удача", "алмаз", "актер", "бухта", "племя")
word = random.choice(words)
max_attempts = 5
used = []
used_and_predicted = []
secret_word = "_" * len(word)

def main(attempts):

    global used
    global used_and_predicted
    global secret_word
    while attempts < max_attempts and secret_word != word:
        print(Fore.CYAN + "Использованные буквы: {}".format(used))
        print(Fore.GREEN + "Угаданные буквы: {} | {:.2f}% прогресса".format(used_and_predicted, len(used_and_predicted) / len(word) * 100))
        print(Fore.RED + "Количество попыток: ", attempts)
        print("Твое слово: ", secret_word)

        user_word = input("Введи слово из 5-ти букв: ")
        if len(user_word) != 5:
            print("Введи слово, состоящее из 5-ти символов!")
            continue

        common_letters_list = check_letters_in_word(user_word, word)
        common_letters_list2 = find_common_letters(common_letters_list, word)
        result = list(set(common_letters_list2) - set(used_and_predicted))
        result2 = list(set(common_letters_list2) - set(used))
        used_and_predicted += [letter for letter in result if letter not in used_and_predicted]
        used += [letter for letter in result2 if letter not in used]
        attempts += 1

        for index, letter in enumerate(word):
            if letter in used_and_predicted:
                secret_word = secret_word[:index] + letter + secret_word[index+1:]

    if attempts == max_attempts:
        print("Ты проиграл, было загадано слово: ", word)
    else:
        print("Ты выиграл, было загадано слово: ", word)

main(attempts=0)