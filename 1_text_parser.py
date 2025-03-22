"""
Instead of using a library to automate whatever you want without understanding
what you are doing (I know you know what I'm talking about), here's a straightforward
script (that has become a little more complex than expected as I kept adding some
edge cases) that will parse a text in different ways.

Even though we could use functions separately and do "function_type(text)"
to parse the target text, I created a class in order to do the .method()
style, like what you get when you do .split(), etc., to show it is feasible
although not what I'd normally do.
"""

# text_file = open("1_text_parser.txt")
# text_sample = text_file.read()
# text_file.close()

with open("1_text_parser.txt", "r", encoding="utf-8") as text_file:
    text_sample = text_file.read()


class TextParser:
    def __init__(self, text):
        self.text = text
        if not isinstance(text, str):
            print("\n\tERROR: NOT A VALID STRING!\n")
            exit()
            # print("Changing invalid input into a string...\n")
            # self.text = str(text)

    def check_punctuation(self):
        """Is a line return \n to be considered as a mark?"""
        punctuation = []
        numbers = "0123456789"
        for character in self.text:
            if (
                not character.isalpha()
                and character not in punctuation
                and character not in numbers
            ):
                # print("NOT alpha:", character)
                punctuation.append(character)
        return punctuation

    def remove_punctuation(self, line_return_status):
        """Here there is the isalpha() method that excludes everything
        that's not a-z A-Z. To use it without compromising the integrity
        of the output text, we must also exclude spaces " " and return
        lines "\n".
        Or we could define a list of the characters we wish to ignore
        and get the output text based on that list."""
        text_as_list = self.make_words_list(line_return=line_return_status)
        if "rreturnn" in text_as_list:
            processed_text = ""
            for w in range(len(text_as_list)):
                word = text_as_list[w]
                if word == "rreturnn":
                    processed_text += "\n"
                else:
                    processed_text += f"{word} "
            return processed_text

        return " ".join(text_as_list)

        for character in self.text:
            if not character.isalpha() and character != " " and character != "\n":
                self.text = self.text.replace(character, "")
        # punct = [".", ",", "?", "!", "...", ":", "(", ")"]
        # for character in punct:
        #     self.text = self.text.replace(character, "")
        return self.text

    def contracted_words(self, word):
        # print("in contracted_words:", word)
        contractions_dict = {
            f"{word[0]}'m": "I am",  # i / I
            f"{word[0]}e's": f"{word[0]}e is",  # h / H
            f"{word[0]}he's": f"{word[0]}he is",  # s / S
            f"{word[0]}e're": f"{word[0]}e are",  # w / W
            f"{word[0]}ou're": f"{word[0]}ou are",  # y / Y
            f"{word[0]}ren't": f"{word[0]}re not",  # a / A
            f"{word[0]}eren't": f"{word[0]}ere not",  # w / W
            "don't": "do not",
            "Don't": "Do not",
            "won't": "will not",
            "Won't": "Will not",
            f"{word[0]}ouldn't": f"{word[0]}uld not",  # w / W / c / C
            f"{word[0]}oesn't": f"{word[0]}oes not",  # d / D
            f"{word[0]}here's": f"{word[0]}here is",
            f"{word[0]}here're": f"{word[0]}here are",
            "lil'": "little",
            "Lil'": "Little",
            "til'": "until",
            "Til'": "Until",
        }
        if word in contractions_dict:
            return contractions_dict[word].split(" ")

    def num_of_nonaplha_chars(self, nonalpha_word):
        return len([char for char in nonalpha_word if not char.isalpha()])

    def make_words_list(self, line_return):
        # self.text = self.text.replace(",", " ,")
        # self.text = self.text.replace(".", " .")
        # self.text = self.text.split()
        # print(self.text)
        """The "problem" of using self.text directly instead of creating an instance
        is that the object then remains affected by the previous used method.
        For example, creating the object texttoparse and using a method on it
        would "save" that object, and any newly applied method would be applied
        on that object and not the texttoparse in its first state (= before applying
        the first method)."""

        text_instance = self.text
        """In a regular text (without special words like ".most_common()"),
        one could directly do the following:"""
        # text_instance = text_instance.replace(",", " ,")
        # text_instance = text_instance.replace(".", " .")
        # text_instance = text_instance.replace(":", " :")
        # text_instance = text_instance.split()

        """Instead, let's convert the text to a list that can be worked on,
        and extract the "special" words, if any."""
        # print("text_instance:", text_instance.split(" "))
        if not line_return:
            text_instance = text_instance.replace("\n", " ")
        else:
            text_instance = text_instance.replace("\n", " rreturnn ")
        text_instance = text_instance.split(" ")
        # print("\n\ttext_instance:\n", text_instance)
        special_words = []

        stop = len(text_instance)
        w = 0
        while stop:
            word = text_instance[w]
            word = word.strip()
            # Removing empty strings to avoid having them in the output list
            if word == "":
                # print("empty word at", w)
                text_instance.remove(word)
                stop -= 1
                continue

            while not word.isalpha():
                # in the order: remove on each side " ", ( )
                if word in special_words:
                    break
                # print("not alpha:", word, w)
                if word.endswith("()") and word.startswith("."):
                    # print("special word:", word)
                    if word.startswith('"') and word.endswith('"'):
                        word = word[1:-1]
                    # print("special word after processing:", word)
                    special_words.append(word)
                    continue

                if word.startswith("-") or word.endswith("-"):
                    word = word.replace("-", "")
                    text_instance[w] = word
                    if word == "":
                        text_instance.remove(word)
                        stop -= 1
                    continue

                if word.startswith('"') or word.endswith('"'):
                    word = word.replace('"', "")
                    text_instance[w] = word
                    continue

                # if word.startswith('"') and word.endswith('"'):
                #     word = word[1:-1]
                #     text_instance[w] = word
                #     continue

                if word.startswith("(") and word.endswith(")"):
                    word = word[1:-1]
                    text_instance[w] = word
                    continue

                if word.endswith("..."):
                    word = word[:-3]
                    text_instance[w] = word
                    continue

                if any(
                    [
                        word.endswith("."),
                        word.endswith(","),
                        word.endswith(":"),
                        word.endswith(")"),
                        word.endswith("?"),
                        word.endswith("!"),
                    ]
                ):
                    # if not word[1].isalpha() and not word[-1].isalpha():
                    # print("word:", word)
                    word = word[:-1]
                    text_instance[w] = word
                    continue

                if any([word.startswith("."), word.startswith("(")]):
                    word = word[1:]
                    text_instance[w] = word
                    continue

                break

            w += 1
            stop -= 1
        # print("special_words:", special_words)
        return text_instance

    def count_words(self):
        text_instance = self.text
        text_instance = self.remove_punctuation(line_return_status=False)
        text_instance = self.text.split()
        return len(text_instance)

    def most_common(self, num_of_words, count_upper=True):
        """That function first removes the punctuation from the given text by
        calling 'remove_punctuation()' (you can add/remove target punctuation
        from that function).
        Depending on the boolean argument 'upper' (True or False), the text
        will keep existing capital letters or change everything into lower
        ones, which will affect the end result, as some would consider the
        words 'For' and 'for' to be the same word.
        The number of displayed words depends on the argument 'num_of_words',
        and cannot be greater than the total number of words and is
        automatically be adjusted.
        """

        upper_result = (
            "The upper letters are NOT ignored"
            if count_upper
            else "The upper letters are ignored"
        )
        text_instance = self.remove_punctuation(line_return_status=False)
        if not count_upper:
            text_instance = text_instance.casefold()
        # print(text_instance)
        text_instance = text_instance.split()
        text_set = set(text_instance)

        words_count = []
        for word in text_set:
            word = word if count_upper else word.casefold()
            words_count.append((word, text_instance.count(word)))
        longest_word = sorted(words_count, key=lambda x: len(x[0]), reverse=True)[0][0]
        # print(longest_word, len(longest_word))
        words_count.sort(key=lambda x: x[1], reverse=True)

        if num_of_words > len(words_count):
            num_of_words = len(words_count)

        title_space_left = int((len(longest_word) - 4) / 2)
        if len(longest_word) % 2 == 0:
            title_space_right = title_space_left - 1
        else:
            title_space_right = title_space_left

        print(f"{num_of_words} MOST COMMON WORDS: ({upper_result})")
        print(f'{" "*title_space_left} WORD {" "*title_space_right}', "OCCURENCES")
        for word in words_count[:num_of_words]:
            word_space_right = len(longest_word) + 12 - len(word[0]) - len(str(word[1]))
            # 12 is the number of characters after the longest word to reach the end of the line
            print(f'{word[0]}{" "* word_space_right}{word[1]}')

    def count_given_words(self, words: list, count_upper=True):
        """That function first removes the punctuation from the given text by
        calling 'remove_punctuation()' (you can add/remove target punctuation
        from that function).
        Depending on the boolean argument 'upper' (True or False), the text
        will keep existing capital letters or change everything into lower
        ones, which will affect the end result, as some would consider the
        words 'For' and 'for' to be the same word.
        The number of displayed words depends on the argument 'num_of_words',
        and cannot be greater than the total number of words and is
        automatically be adjusted.
        """

        if not isinstance(words, list):
            return print('ERROR: Input type is not a list ["word1", "word2", ...]')

        text_instance = self.remove_punctuation(line_return_status=False)
        if not count_upper:
            text_instance = text_instance.casefold()

        words_count = []
        for word in words:
            word = word.strip()
            if word == "":
                return print("ERROR: You cannot leave a word empty.")
            word = word if count_upper else word.casefold()
            words_count.append((word, text_instance.count(word)))
        longest_word = sorted(words_count, key=lambda x: len(x[0]), reverse=True)[0][0]
        words_count.sort(key=lambda x: x[1], reverse=True)

        title_space_left = int((len(longest_word) - 4) / 2)
        if len(longest_word) % 2 == 0:
            title_space_right = title_space_left - 1
        else:
            title_space_right = title_space_left

        selected_words = ", ".join(words)
        print(f'NUMBER OF OCCURENCES FOR THE SELECTED WORD(S): "{selected_words}"')
        print(f'{" "*title_space_left} WORD {" "*title_space_right}', "OCCURENCES")
        for word in words_count:
            word_space_right = len(longest_word) + 12 - len(word[0]) - len(str(word[1]))
            # 12 is the number of characters after the longest word to reach the end of the line
            print(f'{word[0]}{" "* word_space_right}{word[1]}')


text_to_parse = TextParser(text_sample)


print("* * * Text as a list of words with no more punctuation:")
print(text_to_parse.make_words_list(line_return=True))
print()

print("* * * Number of words (including unusual ones such as IP addresses):")
print(f"There are {text_to_parse.count_words()} words in that text.")
print()

print("* * * Punctuation and other non-alpha characters in the text:")
print(text_to_parse.check_punctuation())
print()

# print("* * * Original text:")
# print(text_sample)
# print()

print("* * * Text as original but without punctuation (and with/without line return):")
print(text_to_parse.remove_punctuation(line_return_status=True))
print()

print(
    "* * * Display a chosen number of most common words (taking into account or not capital letters):"
)
text_to_parse.most_common(10, count_upper=True)
print()

print(
    "* * * Display the number of CHOSEN most common words (taking into account or not capital letters):"
)
text_to_parse.count_given_words(
    ["distributions", "frequency", "to", "is", "for", "For", "banana"], count_upper=True
)


# ttt_original = "I like red, yellow and blue. And you?"
# ttt_nomarks = ttt_original
# marks = [",", ".", "?"]
# print(f'Original: "{ttt_original}"')
# for mark in marks:
#     if mark in ttt_nomarks:
#         ttt_nomarks = ttt_nomarks.replace(mark, " ")
# print(f'After replacing marks: "{ttt_nomarks}"')
# ttt_list = ttt_nomarks.split(" ")
# print(f'As a list after split(" "): "{ttt_list}"')
# ttt_list = [mark for mark in ttt_list if mark]
# print(f'Refined list: "{ttt_list}"')
# print(f'Number of words: "{len(ttt_list)}"')
# print(f'Text without punctuation: "{" ".join(ttt_list)}"')
# print(f'No more capital letters: "{" ".join(ttt_list).lower()}"')
# print(f'Number of "and": "{" ".join(ttt_list).lower().count("and")}"')
