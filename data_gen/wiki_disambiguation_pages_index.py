# Loads the link disambiguation index from Wikipedia

data_dir = '/home/wenh/'
path = 'basic_data/wiki_disambiguation_pages.txt'
print('==> Loading disambiguation index')
wiki_disambiguation_index = {}
with open(data_dir+path,'r',encoding='utf8') as f:
    for line in f:
        parts = line.split('\t')
        assert int(parts[0])
        wiki_disambiguation_index[int(parts[0])] = 1

assert wiki_disambiguation_index[579]
assert wiki_disambiguation_index[41535072]

print('    Done loading disambiguation index')
