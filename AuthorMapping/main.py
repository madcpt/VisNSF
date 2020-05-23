import os
import sys
from overrides import overrides

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.COLUMNS import Column
from AuthorMapping.src.AuthorMapper import AuthorMapper
from AuthorMapping.src.AuthorMapper_Direct import DirectMapper
from AuthorMapping.src.AuthorMapper_NameInsti import NameInstitutionMapper


if __name__ == '__main__':
    # mapper = DirectMapper()
    mapper = NameInstitutionMapper()
    result = mapper.run_test()
    print(result)
