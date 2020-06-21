import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.preprocess import load_samples
from AuthorMapping.col_utils import Column


class AuthorMapper(object):
    def __init__(self, load_all=True):
        if load_all:
            self.all_samples = load_samples('./data/NSF_US_data/NSF_US_all.json')
        self.test_samples = load_samples('./data/NSF_US_data/NSF_US_test.json')
        random.shuffle(self.test_samples)
        self._dropout()

    def _dropout(self):
        pass

    def _run_mapping(self, sample: Column):
        # Implement algorithm here
        x = self.test_samples
        return 'author_id here'

    def run_test(self, test_num=500):
        hit, cnt = 0, 0
        import time
        from tqdm import tqdm
        start = time.time()
        for sample in tqdm(self.test_samples[:test_num], total=len(self.test_samples[:test_num])):
            cnt += 1
            matching_result = self._run_mapping(sample)
            if sample.author_id == matching_result:
                hit += 1
        return hit / cnt, time.time() - start

