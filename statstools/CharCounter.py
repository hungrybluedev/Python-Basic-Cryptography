from collections import Counter


class CharCounter:

    def __init__(self):
        self.counter = Counter()
        self.entries = None

        self.default_selector = lambda pair: -pair[1]
        self.selector_function = None

    def add_char(self, character):
        self.counter[character] += 1

    def case_insensitive_add_char(self, character):
        if character.isspace():
            self.add_char("whitespace")
        else:
            self.add_char(character.lower())

    def set_selector_function(self, function):
        self.selector_function = function

    def get_entries(self):
        if not self.entries:
            self.entries = sorted(
                self.counter.items(),
                key=self.selector_function or self.default_selector
            )
        return self.entries

    def __str__(self):
        header = "Character  | Frequency\n-----------+----------\n"
        rows = []

        for k, v in self.get_entries():
            rows.append("{:<10} | {:<9}".format(k, v))

        return header + "\n".join(rows)

    def write_csv_to_file(self, filename):
        output_file = open(filename, "w", encoding="utf-8")
        for k, v in self.get_entries():
            output_file.write("%s,%s\n" % (k, v))

    def get_frequency_map(self):
        return self.counter


if __name__ == '__main__':
    file = open("data/sample.txt", "r", encoding="utf-8")
    text = file.read()

    counter = CharCounter()
    # counter.set_key_selector(lambda x: x[1])

    for char in text:
        counter.case_insensitive_add_char(char)

    print(counter)

    counter.write_csv_to_file("data/output.csv")
