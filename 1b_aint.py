"""
We'll assume ain't is the informal form of ISN'T / AM NOT / AREN'T
Not sure I covered all the use cases, but as you can see it even
processes questions and takes care of non-alpha characters.
"""

text_sample_original = """Ain't that right? It's true, ain't it?
It ain't that easy to parse, and I ain't willing to check all the use cases, they ain't a few!
My neighbor badly injured his back last week, he ain't coming back so soon!
Oooh aren't you a happy dog... Aren't you? Ain't you??! Yea... you aren't. You ain't!"""


def aint_case(text):
    def clean_next_word(next_word):
        """Here we'll assume that the special characters are
        AFTER the pronouns (= punctuation)"""
        if not next_word.isalpha():
            clean_word = ""
            non_alpha = ""
            for char in next_word:
                if char.isalpha():
                    clean_word += char
                else:
                    non_alpha += char
            # print("clean_word:", clean_word, "non_alpha:", non_alpha)
            return clean_word, non_alpha
        return next_word, ""

    use_cases_dict = {
        "it": "is not",
        "this": "is not",
        "that": "is not",
        "he": "is not",
        "she": "is not",
        "we": "are not",
        "you": "are not",
        "they": "are not",
        "these": "are not",
        "those": "are not",
        "i": "am not",
    }

    pronouns_list = [
        "it",
        "this",
        "that",
        "he",
        "she",
        "we",
        "you",
        "they",
        "these",
        "those",
        "i",
    ]

    text_sample = text.replace("\n", " rreturnn ")
    text_sample = text_sample.split(" ")

    for w in range(len(text_sample)):
        word = text_sample[w]

        # if word.lower() == "ain't" or word.lower() == "aren't":
        if "ain't" in word.lower() or "aren't" in word.lower():
            if w == 0:  # It means it's a question as it's starting with Ain't/Aren't
                next_word = text_sample[w + 1].lower()
                linked_verb = use_cases_dict[next_word].split(" ")
                text_sample[w] = f"{linked_verb[0].capitalize()} {next_word}"
                text_sample[w + 1] = linked_verb[1]

            elif not word[-1].isalpha():
                punctuation = ""  # we assume punctuation is always AFTER
                # print("isalpha:", word, w)
                while True:
                    if not word[-1].isalpha():
                        punctuation += word[-1]
                        word = word[:-1]
                        continue

                    previous_word = text_sample[w - 1].lower()
                    if previous_word in pronouns_list:  # normal sentence
                        text_sample[w] = f"{use_cases_dict[previous_word]}{punctuation}"
                    break

            else:
                previous_word = text_sample[w - 1].lower()

                # print("next_word:", next_word)
                # clean_next_word()
                if previous_word in pronouns_list:  # normal sentence
                    text_sample[w] = use_cases_dict[previous_word]
                else:  # swapped positions (may be a question)
                    next_word, non_alpha = clean_next_word(text_sample[w + 1].lower())
                    linked_verb = use_cases_dict[next_word].split(" ")
                    if word[0] == "A":
                        linked_verb[0] = linked_verb[0].capitalize()
                    text_sample[w] = f"{linked_verb[0]} {next_word}"
                    text_sample[w + 1] = f"{linked_verb[1]}{non_alpha}"

    # print("text_sample:")
    # print(text_sample)
    return (" ".join(text_sample)).replace(" rreturnn ", "\n")


parsed_text = aint_case(text_sample_original)


print("* * * Original text:")
print(text_sample_original)
print()
print("* * * Parsed version:")
print(parsed_text)
