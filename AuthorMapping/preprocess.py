import json
import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.col_utils import Column, COLUMNS

csv.field_size_limit(sys.maxsize)


def load_dataset(data_path='./data/NSF_US_data/NSF_US_nsf_mapping2.tsv'):
    all_lines = []
    with open(data_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for line_id, values in enumerate(reader):
            assert len(COLUMNS) - 1 == len(values)
            all_lines.append([line_id] + values)
    return all_lines


def extract_test_samples(all_lines, sample_rate=0.1, data_path='./data/NSF_US_data/'):
    import random
    sampled_lines = []
    rest_lines = []
    for x in all_lines:
        if random.random() < sample_rate:
            sampled_lines.append(x)
        rest_lines.append(x)
    with open(os.path.join(data_path, 'NSF_US_test.json'), 'w') as f:
        json.dump(sampled_lines, f)
    with open(os.path.join(data_path, 'NSF_US_all.json'), 'w') as f:
        json.dump(rest_lines, f)
    return


def load_samples(data_path='./data/NSF_US_data/NSF_US_test.json'):
    with open(data_path, 'r') as f:
        all_lines = json.load(f)
    return [Column(x) for x in all_lines]


def build_graph(all_lines: [Column], dump_path='./data/NSF_US_data/NSF_US_maps.json'):
    author_collaboration_map, inst_authors_map, author_inst_map = {}, {}, {}
    for x in all_lines:
        if len(x.institution) == 0:
            continue
        if x.institution not in inst_authors_map:
            inst_authors_map[x.institution] = []
        inst_authors_map[x.institution].append(x.author_id)
        if x.author_id not in author_inst_map:
            author_inst_map[x.author_id] = []
        if x.institution not in author_inst_map[x.author_id]:
            author_inst_map[x.author_id].append(x.institution)
    dump_obj = {'inst_authors_map': inst_authors_map, 'author_inst_map': author_inst_map}
    # author_collaboration_map = {x: inst_authors_map[author_inst_map[x]] for x in author_inst_map}
    # dump_obj = author_collaboration_map
    with open(dump_path, 'w') as f:
        json.dump(dump_obj, f)
    return


def load_graph(load_path='./data/NSF_US_data/NSF_US_maps.json'):
    with open(load_path, 'r') as f:
        dump_obj = json.load(f)
    # inst_authors_map, author_inst_map = dump_obj['inst_authors_map'], dump_obj['author_inst_map']
    # author_collaboration_map = {x: inst_authors_map[author_inst_map[x]] for x in author_inst_map}
    # author_collaboration_map = {x: inst_authors_map[author_inst_map[x]] for x in author_inst_map}
    # return dump_obj
    # return author_collaboration_map
    return dump_obj['inst_authors_map'], dump_obj['author_inst_map']


if __name__ == '__main__':
    # lines = load_dataset()
    # extract_test_samples(lines)
    # test_samples = load_samples('./data/NSF_US_data/NSF_US_test.json')
    all_samples = load_samples('./data/NSF_US_data/NSF_US_all.json')
    # print(test_samples[0])

    build_graph(all_samples)
    # collaboration_map = load_graph()
    inst_authors_map, author_inst_map = load_graph()
    # print(len(collaboration_map))
