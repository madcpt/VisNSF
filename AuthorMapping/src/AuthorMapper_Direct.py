import os
import sys
from overrides import overrides

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.COLUMNS import Column
from AuthorMapping.src.AuthorMapper import AuthorMapper


class DirectMapper(AuthorMapper):
    def __init__(self):
        super().__init__()
        self.name_id_dict = {}
        for x in self.all_samples:
            if x.name not in self.name_id_dict:
                self.name_id_dict[x.name] = []
            self.name_id_dict[x.name].append(x)

    @overrides
    def _run_mapping(self, sample: Column):
        if sample.name in self.name_id_dict:
            return self.name_id_dict[sample.name][0].id
        # for x in self.all_samples:
        #     if x.name == sample.name:
        #         return x.author_id
        return None


if __name__ == '__main__':
    mapper = DirectMapper()
    result = mapper.run_test()
    print(result)
