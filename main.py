def read_file(filename):
    """Зчитує файл і повертає його вміст як рядок."""
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def count_letters(text):
    """Підраховує кількість кожної літери в тексті, ототожнюючи 'ё' з 'е'."""
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    letter_count = {letter: 0 for letter in alphabet}

    for letter in text:
        if letter == 'ё':
            letter_count['е'] += 1
        elif letter in letter_count:
            letter_count[letter] += 1

    return letter_count


def determine_alphabet_type(letter_count):
    """Визначає тип алфавіту на основі підрахунку літер."""
    has_hard_sign = letter_count['ъ'] > 0
    has_soft_sign = letter_count['ь'] > 0

    if not has_hard_sign:
        return 'alphabet_without_hard_sign'
    elif not has_soft_sign:
        return 'alphabet_without_soft_sign'
    else:
        raise ValueError("Неочікувана конфігурація алфавіту")


def form_alphabet_array(alphabet_type):
    """Формує масив алфавіту відповідно до типу алфавіту."""
    if alphabet_type == 'alphabet_without_hard_sign':
        alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
    elif alphabet_type == 'alphabet_without_soft_sign':
        alphabet = 'абвгдежзийклмнопрстуфхцчшщъыэюя'
    else:
        raise ValueError("Неочікуваний тип алфавіту")

    alphabet_array = {letter: index for index, letter in enumerate(alphabet)}

    return alphabet_array


def print_results(letter_count, alphabet_array, total_letters):
    """Виводить результати."""
    print("Кількість літер у тексті:")
    for letter, count in letter_count.items():
        print(f"{letter}: {count}")

    print("\nМасив алфавіту:")
    for letter, index in alphabet_array.items():
        print(f"{letter}: {index}")

    print(f"\nВсього літер у шифротексті: {total_letters}")


def main():
    filename = input("Введіть шлях до текстового файлу: ")
    text = read_file(filename)
    letter_count = count_letters(text)
    alphabet_type = determine_alphabet_type(letter_count)
    alphabet_array = form_alphabet_array(alphabet_type)
    total_letters = sum(letter_count.values())
    print_results(letter_count, alphabet_array, total_letters)


if __name__ == "__main__":
    main()
