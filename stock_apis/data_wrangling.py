class JankyCSV(object):
    def __init__(self, data, delimiter='\n'):
        self.data = data.split(delimiter)

    @staticmethod
    def sanitize_row(row):
        remove_characters = ['"', '\n', '\r']
        for char in remove_characters:
            row = row.replace(char, '')
        return row

    @staticmethod
    def __csv_generator(data, delimiter):
        for row in data:
            if row:
                yield [JankyCSV.sanitize_row(x) for x in row.split(delimiter) if JankyCSV.sanitize_row(x)]

    def get_rows(self, delimiter, include_headers=False):
        if include_headers:
            return JankyCSV.__csv_generator(self.data, delimiter)

        return JankyCSV.__csv_generator(self.data[1:], delimiter)
