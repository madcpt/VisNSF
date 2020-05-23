COLUMNS = ["line_id", "author_id", "first_name", "last_name", "name", "institution", "amount", "code", "instrument",
           "directorate", "year", "title", "division", "date_1", "date_2"]

CHAR_DROPOUT_RATE = 0.2
INSTITUTION_DROPOUT_RATE = 0.8


class Column(object):
    author_id = 0
    first_name = 1
    last_name = 2
    name = 3
    institution = 4
    amount = 5
    code = 6
    instrument = 7
    directorate = 8
    year = 9
    title = 10
    division = 11
    date_1 = 12
    date_2 = 13

    def __init__(self, values):
        assert len(values) == len(COLUMNS)
        for i, c in enumerate(COLUMNS):
            self.__setattr__(c, values[i])
