from Utils.utils import *

data_dir = '/home/wenh/'
print("==> Loading redirects index")
path = data_dir + 'basic_data/wiki_redirects.txt'

with open(path,'r',encoding='utf8') as f:
    wiki_redirects_index = {}
    for line in f:
        parts = line.split('\t')
        wiki_redirects_index[parts[0]] = parts[1].strip()

assert wiki_redirects_index['Coercive']=='Coercion'
assert wiki_redirects_index['Hosford, FL'] == 'Hosford, Florida'

print('    Done loading redirects index')

def get_redirected_ent_title(ent_name):
    if wiki_redirects_index.get(ent_name):
        return wiki_redirects_index[ent_name]
    else:
        return ent_name

if __name__ == '__main__':
    if get_redirected_ent_title:
        ent_name = get_redirected_ent_title('Coercive')
        print(ent_name)