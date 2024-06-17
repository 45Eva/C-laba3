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


def count_bigrams(text, alphabet_array):
    """Підраховує кількість неперетинних біграм у тексті."""
    size = len(alphabet_array)
    bigram_matrix = [[0] * size for _ in range(size)]

    for i in range(0, len(text) - 1, 2):
        first_letter = text[i]
        second_letter = text[i + 1]

        if first_letter == 'ё':
            first_letter = 'е'
        if second_letter == 'ё':
            second_letter = 'е'

        if first_letter in alphabet_array and second_letter in alphabet_array:
            row = alphabet_array[first_letter]
            col = alphabet_array[second_letter]
            bigram_matrix[row][col] += 1

    return bigram_matrix


def get_top_5_bigrams(bigram_matrix, alphabet_array):
    """Знаходить 5 найпоширеніших біграм у матриці."""
    bigrams = []
    alphabet_list = list(alphabet_array.keys())

    for i in range(len(bigram_matrix)):
        for j in range(len(bigram_matrix[i])):
            bigrams.append(((alphabet_list[i], alphabet_list[j]), bigram_matrix[i][j]))

    bigrams.sort(key=lambda x: x[1], reverse=True)
    top_5_bigrams = bigrams[:5]

    return top_5_bigrams


def print_results(letter_count, alphabet_array, total_letters, top_5_bigrams, bigram_matrix):
    """Виводить результати."""
    print("Кількість літер у тексті:")
    for letter, count in letter_count.items():
        print(f"{letter}: {count}")

    print("\nМасив алфавіту:")
    for letter, index in alphabet_array.items():
        print(f"{letter}: {index}")

    print(f"\nВсього літер у шифротексті: {total_letters}")

    print("\n5 найпоширеніших біграм:")
    for bigram, count in top_5_bigrams:
        print(f"{bigram}: {count}")

    print("\nМатриця біграм:")
    alphabet_list = list(alphabet_array.keys())
    print("    " + " ".join(alphabet_list))
    for i, row in enumerate(bigram_matrix):
        print(f"{alphabet_list[i]} " + " ".join(f"{count:2}" for count in row))


def extended_gcd(a, b):
    """Розширений алгоритм Евкліда. Повертає (gcd, x, y), де gcd - найбільший спільний дільник a та b, і x, y такі, що ax + by = gcd"""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def mod_inverse(a, n):
    """Обчислює обернений елемент для a за модулем n, якщо він існує."""
    gcd, x, y = extended_gcd(a, n)
    if gcd != 1:
        raise ValueError(f"Обернений елемент не існує для {a} за модулем {n}")
    return x % n


def solve_linear_congruence(a, b, n):
    """
    Розв'язує лінійне порівняння ax ≡ b (mod n).
    Повертає список усіх розв'язків, якщо вони існують, або порожній список, якщо розв'язків немає.
    """
    gcd, x, _ = extended_gcd(a, n)
    if b % gcd != 0:
        return []  # Немає розв'язків

    a1 = a // gcd
    b1 = b // gcd
    n1 = n // gcd
    x0 = (x * b1) % n1  # Один розв'язок

    # Генеруємо всі розв'язки
    solutions = [(x0 + i * n1) % n for i in range(gcd)]
    return solutions


def main():
    filename = input("Введіть шлях до текстового файлу: ")
    text = read_file(filename)
    letter_count = count_letters(text)
    alphabet_type = determine_alphabet_type(letter_count)
    alphabet_array = form_alphabet_array(alphabet_type)
    bigram_matrix = count_bigrams(text, alphabet_array)
    top_5_bigrams = get_top_5_bigrams(bigram_matrix, alphabet_array)
    total_letters = sum(letter_count.values())
    print_results(letter_count, alphabet_array, total_letters, top_5_bigrams, bigram_matrix)

    russian_bigrams = [('с', 'т'), ('н', 'о'), ('т', 'о'), ('н', 'а'), ('е', 'н')]
    for bigram in russian_bigrams:
        print(f"Російська біграма: {bigram}")


if __name__ == "__main__":
    main()
