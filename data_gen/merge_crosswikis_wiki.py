# Merge Wikipedia and Crosswikis p(e|m) indexes
# Run: python data_gen/gen_p_e_m/merge_crosswikis_wiki.py

import sys
sys.path.append('/home/wenh/deep-el')
from entities.ent_name_id import *

print('\nMerging Wikipedia and Crosswikis p_e_m')
merged_e_m_counts = {}

print('Process Wikipedia')

data_dir = '/home/wenh/'
path = data_dir + 'generated/wikipedia_p_e_m.txt'

with open(path,'r',encoding='utf8') as f:
    for line in f:
        parts = line.split('\t')
        mention = parts[0]

        if not mention.find('Wikipedia') + 1 and not mention.find('wikipedia') + 1:
            if mention not in merged_e_m_counts.keys():
                merged_e_m_counts[mention] = {}

            total_freq = int(parts[1])
            assert total_freq
            num_ents = len(parts)
            for i in range(2,num_ents-1):
                ent_str = parts[i].split(',')
                ent_wikiid = int(ent_str[0])
                assert ent_wikiid
                freq = int(ent_str[1])
                assert freq

                if ent_wikiid not in merged_e_m_counts[mention].keys():
                    merged_e_m_counts[mention][ent_wikiid] = 0

                merged_e_m_counts[mention][ent_wikiid] = merged_e_m_counts[mention][ent_wikiid] + freq

print('Process Crosswikis')

path_cross = data_dir + 'basic_data/p_e_m_data/crosswikis_p_e_m.txt'

with open(path_cross,'r',encoding='utf8') as f:
    for line in f:
        parts = line.split('\t')
        mention = parts[0]
        if not mention.find('Wikipedia')+1 and not mention.find('wikipedia')+1:
            if mention not in merged_e_m_counts.keys():
                merged_e_m_counts[mention] = {}

            total_freq = int(parts[1])
            assert total_freq
            num_ents = len(parts)
            for i in range(2,num_ents-1):
                ent_str = parts[i].split(',')
                ent_wikiid = int(ent_str[0])
                assert ent_wikiid
                freq = int(ent_str[1])
                assert freq

                if ent_wikiid not in merged_e_m_counts[mention].keys():
                    merged_e_m_counts[mention][ent_wikiid] = 0
                merged_e_m_counts[mention][ent_wikiid]=merged_e_m_counts[mention][ent_wikiid] + freq

print('Now sorting and writing ..')
out_file = data_dir + 'generated/crosswikis_wikipedia_p_e_m.txt'
ouf = open(out_file,'w')

for mention,lst in merged_e_m_counts.items():
    if len(mention) >= 1 :
        tbl = []
        for ent_wikiid,freq in lst.items():
            t = {}
            t['ent_wikiid'] = ent_wikiid
            t['freq'] = freq
            tbl.append(t)
        tbl = sorted(tbl, key=lambda x: x["freq"], reverse=True)

        strs = ''
        total_freq = 0
        num_ents = 0
        for el in tbl:
            if is_valid_ent(el['ent_wikiid']):
                strs = strs + str(el['ent_wikiid']) + ',' + str(el['freq'])
                strs = strs + ',' + get_ent_name_from_wikiid(el['ent_wikiid']).replace(' ', '_') + '\t'
                num_ents = num_ents + 1
                total_freq = total_freq + el['freq']

                if num_ents >= 100 : # At most 100 candidates
                    break
        ouf.write(mention + '\t' + str(total_freq) + '\t' + strs + '\n')
ouf.flush()
ouf.close()

print('    Done sorting and writing.')


