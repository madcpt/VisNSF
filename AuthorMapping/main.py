import os
import sys
from overrides import overrides

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.COLUMNS import Column
from AuthorMapping.src.AuthorMapper import AuthorMapper
from AuthorMapping.src.AuthorMapper_NameDirect import NameDirectMapper
from AuthorMapping.src.AuthorMapper_NameInstDirect import NameInstitutionDirectMapper
from AuthorMapping.src.AuthorMapper_NameLevenshtein import NameBLEUMapper
from AuthorMapping.src.AuthorMapper_NameInstLevenshtein import NameInstBLEUMapper


if __name__ == '__main__':
    # mapper = NameDirectMapper()
    # mapper = NameInstitutionDirectMapper()
    # mapper = NameBLEUMapper()
    mapper = NameInstBLEUMapper()
    result = mapper.run_test()
    print(result)

