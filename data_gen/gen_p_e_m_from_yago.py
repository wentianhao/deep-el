import sys
sys.path.append('/home/wenh/deep-el')
from data_gen.unicode_map import unicode2ascii
from entities.ent_name_id import *

data_dir = '/home/wenh/'
path = data_dir + 'basic_data/p_e_m_data/aida_means.tsv'

num_lines = 0
wiki_e_m_counts = {}

print('\nComputing YAGO p_e_m')

with open(path,'r',encoding='utf8') as f:
    for line in f :
        num_lines = num_lines + 1
        if num_lines % 5000000 == 0 :
            print('Processed' + str(num_lines) + ' lines.')
        parts = line.split('\t')
        assert len(parts) == 2
        assert  parts[0][0] == '"'
        assert parts[0][len(parts[0])-1] == '"'

        mention = parts[0][1:len(parts[0])-2]
        ent_name = parts[1]
        ent_name = ent_name.replace('&amp;','&')
        ent_name = ent_name.replace('&quot;','"')
        while ent_name.find('\\u') + 1:
            x = ent_name.find('\\u')
            code = ent_name[x:x+6]
            re = unicode2ascii[code]
            # assert unicode2ascii[code]
            if re == '%':
                re = '%%'
            ent_name = ent_name.replace(code,re)

        ent_name = preprocess_ent_name(ent_name)
        ent_wikiid = get_ent_wikiid_from_name(ent_name,True)
        if ent_wikiid != unk_ent_wikiid:
            if not mention in wiki_e_m_counts.keys():
                wiki_e_m_counts[mention] = {}
            wiki_e_m_counts[mention][ent_wikiid] = 1

print('Now sorting and writing ..')
out_file = data_dir + 'generated/yago_p_e_m.txt'
ouf = open(out_file,'w')

for mention,lst in wiki_e_m_counts.items():
    strs = ''
    total_freq = 0
    for ent_wikiid in lst:
        strs = strs + str(ent_wikiid) + ','+get_ent_name_from_wikiid(ent_wikiid).replace(' ','_')+'\t'
        total_freq = total_freq + 1
    ouf.write(mention +'\t'+str(total_freq)+'\t'+strs+'\n')
ouf.flush()
ouf.close()

print('    Done sorting and writing.')