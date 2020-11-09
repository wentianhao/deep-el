import torch
import re

'''
:param one_dim_tensor: 
:param k: 
:return: 
'''
def topK(one_dim_tensor,k):
    bestk , indices = torch.topk(one_dim_tensor,k=k)
    # print("bestk:",bestk)
    # print("indices:",indices)
    sorts , newindices = torch.sort(bestk,descending=True)
    # print("sorts:",sorts)
    # print("newindices:",newindices)
    oldindices = torch.LongTensor(k)
    # print("oldindices:",oldindices)

    for i in range(0,k):
        oldindices[i] = indices[0,newindices[0,i]]
    return sorts,oldindices

def table_len(t):
    count = 0
    for _ in t :
        count = count + 1
    return count

# 去掉首尾的两边的空格
def trim1(s):
    return s.strip()

# 首字母大写
def first_letter_to_uppercase(s):
    return s[0].upper()+s[1:]

if __name__ == '__main__':
    one_dim = torch.rand(1,8)
    # print("one_dim:",one_dim)
    # sorts , oldindices = topK(one_dim,5)
    # print("oldindices:",oldindices)
    # if not table_len:
    #     print('')
    s = 'a<doc xAsdada'
    x= s.find('<doc')
    y = int(x) + len('<doc')
    # print(x,y)
    ss = s[0:-1]
    # print(ss)
    xx = first_letter_to_uppercase(s)
    print(xx)