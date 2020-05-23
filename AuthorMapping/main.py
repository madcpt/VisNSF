import os
import sys
from overrides import overrides

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.col_utils import Column
from AuthorMapping.src.AuthorMapper import AuthorMapper
from AuthorMapping.src.AuthorMapper_NameDirect import NameDirectMapper
from AuthorMapping.src.AuthorMapper_NameInstDirect import NameInstitutionDirectMapper
from AuthorMapping.src.AuthorMapper_NameLevenshtein import NameBLEUMapper
from AuthorMapping.src.AuthorMapper_NameInstLevenshtein import NameInstBLEUMapper
from AuthorMapping.src.AuthorMapper_NameCol import NameColMapper
from AuthorMapping.src.AuthorMapper_NameColGNN import NameColGNNMapper


if __name__ == '__main__':
    # mapper = NameInstitutionDirectMapper()
    # mapper = NameBLEUMapper()
    # mapper = NameInstBLEUMapper()
    # mapper = NameDirectMapper()
    # mapper = NameColMapper()
    mapper = NameColGNNMapper()

    import torch
    for i in range(10):
        l = mapper.train_epoch()
        try:
            torch.save(mapper.mapper_model, '%d.model' % i)
        except:
            pass
        result = mapper.run_test()
        print(i, l, result)


