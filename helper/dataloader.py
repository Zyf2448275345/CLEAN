import torch
import random
from helper.utils import format_esm

def mine_negative(anchor, id_ec, ec_id, mine_neg):
    anchor_ec = id_ec[anchor]
    pos_ec = random.choice(anchor_ec)
    neg_ec = mine_neg[pos_ec]['negative']
    weights = mine_neg[pos_ec]['weights']
    result_ec = random.choices(neg_ec, weights=weights, k=1)[0]
    while result_ec in anchor_ec:
        result_ec = random.choices(neg_ec, weights=weights, k=1)[0]
    neg_id = random.choice(ec_id[result_ec])
    return neg_id

def random_positive(id, id_ec, ec_id):
    pos_ec = random.choice(id_ec[id])
    pos = id
    if len(ec_id[pos_ec]) == 1:
        return pos + '_' + str(random.randint(0,9))
    while pos == id:
        pos = random.choice(ec_id[pos_ec])
    return pos
    
class Dataset_with_mine_EC(torch.utils.data.Dataset):

    def __init__(self, id_ec, ec_id, mine_neg):
        self.id_ec = id_ec
        self.ec_id = ec_id
        self.full_list = []
        self.mine_neg = mine_neg
        for ec in ec_id.keys():
            if '-' not in ec:
                self.full_list.append(ec)
    
    def __len__(self):
        return len(self.full_list)
    
    def __getitem__(self,index):
        anchor_ec = self.full_list[index]
        anchor = random.choice(self.ec_id[anchor_ec])
        pos = random_positive(anchor, self.id_ec, self.ec_id)
        neg = mine_negative(anchor, self.id_ec, self.ec_id, self.mine_neg)
        a = torch.load('./data/esm_data/' + anchor + '.pt')
        p = torch.load('./data/esm_data/' + pos + '.pt')
        n = torch.load('./data/esm_data/' + neg + '.pt')
        return format_esm(a), format_esm(p), format_esm(n) 