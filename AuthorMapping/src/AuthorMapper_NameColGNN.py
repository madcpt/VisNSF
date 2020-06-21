import os
import random
import sys
from overrides import overrides

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from AuthorMapping.col_utils import Column, CHAR_DROPOUT_RATE, COLLABORATION_AVAILABLE_RATE
from AuthorMapping.src.AuthorMapper import AuthorMapper
from AuthorMapping.preprocess import load_graph

import torch
from torch import nn
import numpy as np
from dgl.nn.pytorch import GraphConv
from dgl import DGLGraph


class GCN(nn.Module):
    def __init__(self, in_feats, hidden_size, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GraphConv(in_feats, hidden_size)
        self.conv2 = GraphConv(hidden_size, num_classes)

    def forward(self, g, inputs):
        h = self.conv1(g, inputs)
        h = torch.relu(h)
        h = self.conv2(g, h)
        return h


class Mapper(nn.Module):
    def __init__(self, author_list: list):
        super().__init__()
        self.author_list = author_list
        self.author_map = {x: i for i, x in enumerate(author_list)}
        self.node_embedding = nn.Embedding(len(self.author_list), 32)
        self.char_embedding = nn.Embedding(27, 32)
        self.char_rnn = nn.GRU(input_size=32, hidden_size=32, batch_first=True)
        self.GCN_layer = GCN(32, 16, 8)
        self.similarity_att = nn.Linear(8, 8)

    def _parse_string(self, name: str):
        char_ids = [ord(x) - ord('a') + 1 for x in name.lower()]
        char_ids = [x if 1 <= x <= 26 else 0 for x in char_ids]
        char_embed = self.char_embedding.weight[char_ids].unsqueeze(dim=0)
        _, name_emb = self.char_rnn(char_embed)
        name_emb = name_emb.squeeze(dim=0)
        assert name_emb.size(0) == 1 and name_emb.size(1) == 32
        return name_emb

    def build_graph(self, target_author, target_author_cols, sample_author_name, sample_author_cols_name):
        target_author_idx = self.author_map[target_author]
        target_author_cols_idx = [self.author_map[x] for x in target_author_cols]
        target_author_embed = self.node_embedding.weight[target_author_idx].unsqueeze(dim=0)
        target_author_cols_embed = self.node_embedding.weight[target_author_cols_idx]
        sample_author_embed = self._parse_string(sample_author_name)
        sample_author_cols_embed = torch.cat([self._parse_string(x) for x in sample_author_cols_name], dim=0)
        inputs = torch.cat(
            [target_author_embed, sample_author_embed, target_author_cols_embed, sample_author_cols_embed])
        src, dst = [], []
        for i in range(len(target_author_cols)):
            src.append(0)
            dst.append(i + 1)
        for i in range(len(sample_author_cols_name)):
            src.append(1)
            dst.append(i + len(target_author_cols) + 2)
        src, dst = np.array(src), np.array(dst)
        u = np.concatenate([src, dst])
        v = np.concatenate([dst, src])
        output = self.GCN_layer(DGLGraph((u, v)), inputs)
        score = torch.matmul(output[[0]], output[[1]].T)
        assert score.size(0) == 1 and score.size(1) == 1
        return output, score


class NameColGNNMapper(AuthorMapper):
    def __init__(self):
        super().__init__()
        self.name_id_dict = {}
        self.id_name_dict = {}
        for x in self.all_samples:
            if x.name not in self.name_id_dict:
                self.name_id_dict[x.name] = []
            self.name_id_dict[x.name].append(x)
            self.id_name_dict[x.author_id] = x.name
        inst_authors_map, author_inst_map = load_graph()
        # self.collaboration_map = load_graph()
        self.collaboration_map = {}
        for k, v in author_inst_map.items():
            self.collaboration_map[k] = []
            for inst in v:
                self.collaboration_map[k].extend(inst_authors_map[inst])

        for x in self.all_samples:
            if x.author_id in self.collaboration_map:
                x.collaborators = self.collaboration_map[x.author_id]
        for x in self.test_samples:
            if x.author_id in self.collaboration_map:
                x.collaborators = [t for t in self.collaboration_map[x.author_id] if
                                   random.random() < COLLABORATION_AVAILABLE_RATE]
        self.mapper_model = Mapper([x for x in author_inst_map]).cuda()
        self.optimizer = torch.optim.Adam(self.mapper_model.parameters(), lr=0.01)
        self.loss_f = nn.BCEWithLogitsLoss()

    @overrides
    def _dropout(self):
        # for x in self.test_samples:
        #     name_new = ''
        #     for char in x.name:
        #         if random.random() >= CHAR_DROPOUT_RATE:
        #             name_new += char
        #     x.name = name_new
        pass

    @overrides
    def _run_mapping(self, sample: Column):
        try:
            if sample.name in self.name_id_dict:
                max_score, max_target_id = 0, None
                for target in self.name_id_dict[sample.name]:
                    target_id = target.author_id
                    sample_cols_name = [self.id_name_dict[x] for x in sample.collaborators if x in self.id_name_dict]
                    _, score = self.mapper_model.build_graph(target_id, self.collaboration_map[target_id], sample.name,
                                                             sample_cols_name)
                    if score.cpu().item() > max_score:
                        max_score = score.cpu().item()
                        max_target_id = target_id
                if max_target_id:
                    return max_target_id
        except:
            pass
        return None

    def train_epoch(self, test_num=500):
        l = 0
        self.mapper_model.train()
        from tqdm import tqdm
        # for sample in tqdm(self.all_samples, total=len(self.all_samples)):
        for sample in tqdm(self.test_samples[:test_num], total=test_num):
            try:
                if sample.name in self.name_id_dict:
                    scores, labels = [], []
                    for target in self.name_id_dict[sample.name]:
                        target_id = target.author_id
                        sample_cols_name = [self.id_name_dict[x] for x in sample.collaborators if x in self.id_name_dict]
                        output, score = self.mapper_model.build_graph(target_id, self.collaboration_map[target_id],
                                                                      sample.name,
                                                                      sample_cols_name)
                        scores.append(score)
                        labels.append(target.author_id == sample.author_id)
                    scores = torch.stack(scores).squeeze(dim=-1).squeeze(dim=-1)
                    labels = torch.tensor(labels).cuda().float()
                    try:
                        assert scores.shape == labels.shape
                    except:
                        print(scores.shape, labels.shape)
                        exit()
                    loss = self.loss_f(scores, labels)
                    loss.backward()
                    self.optimizer.step()
                    self.optimizer.zero_grad()
                    l += loss.detach().cpu().item()
            except:
                # print(scores, labels)
                self.mapper_model.zero_grad()
        self.mapper_model.eval()
        return l / len(self.all_samples)


if __name__ == '__main__':
    mapper = NameColMapper()
    result = mapper.run_test()
    print(result)
