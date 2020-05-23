import os
import random
import sys
from overrides import overrides
from nltk.translate.bleu_score import sentence_bleu
import difflib
import Levenshtein

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.col_utils import Column, CHAR_DROPOUT_RATE, INSTITUTION_DROPOUT_RATE
from AuthorMapping.src.AuthorMapper import AuthorMapper


class NameInstBLEUMapper(AuthorMapper):
    def __init__(self):
        super().__init__()
        # self.name_id_dict = {}
        # for x in self.all_samples:
        #     if x.name not in self.name_id_dict:
        #         self.name_id_dict[x.name] = []
        #     self.name_id_dict[x.name].append(x)

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
        # if sample.name in self.name_id_dict:
        #     return self.name_id_dict[sample.name][0].author_id
        max_score, max_author_id = 0, None
        for x in self.all_samples:
            # score = difflib.SequenceMatcher(None, x.name, sample.name).ratio()
            score = Levenshtein.ratio(x.name + x.institution, sample.name + sample.institution)
            # name_score = Levenshtein.ratio(x.name , sample.name)
            # inst_score = Levenshtein.ratio(x.institution, sample.institution)
            # score = name_score + inst_score
            # print(name_score, inst_score)
            # print(score)
            # gold = [[t for t in x.name]]
            # pred = [t for t in sample.name]
            # score = sentence_bleu(gold, pred)
            if score > max_score:
                max_score = score
                max_author_id = x.author_id
        return max_author_id


if __name__ == '__main__':
    mapper = NameBLEUMapper()
    result = mapper.run_test()
    print(result)
