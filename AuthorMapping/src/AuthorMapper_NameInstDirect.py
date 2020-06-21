import os
import random
import sys
from overrides import overrides

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.col_utils import Column, CHAR_DROPOUT_RATE, INSTITUTION_DROPOUT_RATE
from AuthorMapping.src.AuthorMapper import AuthorMapper


class NameInstitutionDirectMapper(AuthorMapper):
    def __init__(self):
        super().__init__()
        self.name_id_dict = {}
        for x in self.all_samples:
            if x.name not in self.name_id_dict:
                self.name_id_dict[x.name] = []
            self.name_id_dict[x.name].append(x)

    @overrides
    def _dropout(self):
        for x in self.test_samples:
            name_new = ''
            for char in x.name:
                if random.random() >= CHAR_DROPOUT_RATE:
                    name_new += char
            x.name = name_new

            if random.random() < INSTITUTION_DROPOUT_RATE:
                x.institution = ''
            else:
                name_new = ''
                for char in x.institution:
                    if random.random() >= CHAR_DROPOUT_RATE:
                        name_new += char
                x.institution = name_new

    @overrides
    def _run_mapping(self, sample: Column):
        if sample.name in self.name_id_dict:
            for x in self.name_id_dict[sample.name]:
                if x.institution.__len__() > 0 and x.institution == sample.institution:
                    return x.author_id
            return self.name_id_dict[sample.name][0].author_id
        # for x in self.all_samples:
        #     if x.name == sample.name:
        #         return x.author_id
        return None


if __name__ == '__main__':
    mapper = NameInstitutionDirectMapper()
    result = mapper.run_test()
    print(result)
