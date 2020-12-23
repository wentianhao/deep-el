# Create a file that contains entity frequencies

from Utils.utils import *
from entities.ent_name_id import *

entity_freqs = {}

num_lines = 0

with open(data_dir+'generated/crosswikis_wikipedia_p_e_m.txt','r',encoding='utf8') as f:
    for line in f:
        num_lines = num_lines + 1
        if num_lines % 2000000 == 0:
            print('Processed ' + str(num_lines) + ' lines.')

        parts = line.rstrip().split('\t')
        num_parts = len(parts)
        for i in range(2,num_parts):
            ent_str = parts[i].split(',')
            ent_wikiid = int(ent_str[0])
            freq = int(ent_str[1])
            assert ent_wikiid
            assert freq

            if not entity_freqs.get(ent_wikiid):
                entity_freqs[ent_wikiid] = 0
            entity_freqs[ent_wikiid] = entity_freqs[ent_wikiid] + freq

# writing word frequencies
print('Sorting and writing')
sorted_ent_freq = []
for ent_wikiid,freq in entity_freqs.items():
    if freq >= 10:
        ent_freq = {'ent_wikiid':ent_wikiid,'freq':freq}
        sorted_ent_freq.append(ent_freq)

sorted(sorted_ent_freq,key=lambda x: x['freq'], reverse=True)

out_file = data_dir + 'generated/ent_wiki_freq.txt'
ouf = open(out_file,'w')
total_freq = 0
for x in sorted_ent_freq:
    ouf.write(str(x['ent_wikiid'])+'\t'+get_ent_name_from_wikiid(x['ent_wikiid'])+'\t'+str(x['freq'])+'\n')
    total_freq = total_freq + x['freq']
ouf.flush()
ouf.close()

print('Total freq= ' + str(total_freq)+'\n')