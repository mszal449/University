import os


# Load words into set

def read_words(filename: str) -> (set, int):
    res_set = set()
    max_len = 0
    with open(filename, "r") as file:
        for line in file:
            word = line.strip()
            if len(word) > max_len: max_len = len(word)
            res_set.add(word)

    return res_set, max_len

def split_row(text: str, words: set, max_word_len: int):
    n = len(text)
    dp = [-1] * (n + 1)
    splits = [-1] * (n + 1)

    # Iterate over whole text
    for i in range(1, n + 1):
        for j in range(max(0, i - max_word_len), i):
            word = text[j:i]

            if word in words:
                score = dp[j] + len(word) ** 2
                if score > dp[i]:
                    dp[i] = score
                    splits[i] = j

    if dp[n] == - 1:
        return text

    result = []
    i = n
    while i > 0:
        j = splits[i]
        result.append(text[j:i])
        i = j
    return " ".join(reversed(result))

print(os.getcwd())
words, max_len = read_words("./task2/words_for_ai1.txt")

with open("zad2_input.txt", 'r') as in_file:
    with open("zad2_output.txt", 'w') as out_file:
        for line in in_file:
            out_file.write(split_row(line.strip(), words, max_len) + '\n')

