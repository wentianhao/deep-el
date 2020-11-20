'''
Each entity has:
a) a Wikipedia URL refferred as 'name' here
b) a Wikipedia ID refferred as 'ent_wikiid' or 'wikiid' here
c) an ID that will be used in the entity embeddings lookup table. Referred as 'ent_thid' or 'thid' there
'''

import Utils.utils as tl
import data_gen.wiki_redirects_index as wri
import data_gen.wiki_disambiguation_pages_index as wdpi
import torch
import os
import entities.relatedness

unk_ent_wikiid = 1
rltd_only = False
ent_type = 'RLTD'
if ent_type and ent_type!='ALL':
    rltd_only =True

# Unk entity wikiid
unk_ent_wikiid = 1

entity_wiki_txtfilename = '/home/wenh/'+'basic_data/wiki_name_id_map.txt'
entity_wiki_t7filename = '/home/wenh/'+'generated/ent_name_id_map.t7'
if rltd_only:
    entity_wiki_t7filename = '/home/wenh/' + 'generated/ent_name_id_map_RLTD.t7'

print('==> Loading entities wikiid - name map')

e_id_name = None

if os.path.exists(entity_wiki_t7filename):
    print(' ---> from t7 file: '+ entity_wiki_t7filename)
    e_id_name = torch.load(entity_wiki_t7filename)
else:
    print('  ---> t7 file NOT found. Loading from disk (slower). Out f = '+ entity_wiki_t7filename)
    import data_gen.wiki_disambiguation_pages_index as wdpi
    print('    Still loading entities wikiid - name map ...')

    e_id_name = {}

    # map for entity name to entity wiki id
    ent_wikiid2name = {}
    ent_name2wikiid = {}

    # map for entity wiki id to tensor id. Size = 4.4M
    if not rltd_only:
        ent_wikiid2thid = {}
        ent_thid2wikiid = {}

    cnt = 0
    cnt_freq = 0
    with open(entity_wiki_txtfilename,'r',encoding='utf8') as f:
        for line in f:
            parts = line.split('\t')
            ent_name = parts[0]
            ent_wikiid = int(parts[1])

            if not ent_wikiid in wdpi.wiki_disambiguation_index:
                if not rltd_only or True :
                    ent_wikiid2name[ent_wikiid] = ent_name
                    ent_name2wikiid[ent_name] = ent_wikiid
                    e_id_name['ent_wikiid2name'] = ent_wikiid2name
                    e_id_name['ent_name2wikiid'] = ent_name2wikiid
                if not rltd_only:
                    cnt = cnt + 1
                    e_id_name['ent_wikiid2thid'][ent_wikiid] = cnt
                    e_id_name['ent_thid2wikiid'][cnt] = ent_wikiid
    if not rltd_only:
        cnt = cnt + 1
        e_id_name['ent_wikiid2thid'][ent_wikiid] = cnt
        e_id_name['ent_thid2wikiid'][cnt] = ent_wikiid

    e_id_name['ent_wikiid2name'][unk_ent_wikiid] = 'UNK_ENT'
    e_id_name['ent_name2wikiid']['UNK_ENT'] = unk_ent_wikiid

    torch.save(e_id_name,entity_wiki_t7filename)

if not rltd_only:
    unk_ent_wikiid = e_id_name['ent_wikiid2thid'][unk_ent_wikiid]
else:
    unk_ent_wikiid = 1 # 之后再写




def preprocess_ent_name(ent_name):
    ent_name = tl.trim1(ent_name)
    ent_name = ent_name.replace('&amp;', '&')
    ent_name = ent_name.replace('&quot;', '"')
    ent_name = ent_name.replace('_', ' ')
    if ent_name == ' ' or ent_name == '':
        return ent_name
    ent_name= tl.first_letter_to_uppercase(ent_name)
    if wri.get_redirected_ent_title:
        ent_name = wri.get_redirected_ent_title(ent_name)
    return ent_name

def get_ent_wikiid_from_name(ent_name,not_verbose):
    verbose = (not not_verbose)
    ent_name = preprocess_ent_name(ent_name)
    if ent_name in e_id_name['ent_name2wikiid'].keys():
        ent_wikiid = e_id_name['ent_name2wikiid'][ent_name]
    else:
        ent_wikiid = 0
    if not ent_wikiid or not ent_name:
        if verbose:
            print('Entity '+ent_name+' not found. Redirects file needs to be loaded for better performance.')
        return unk_ent_wikiid
    return ent_wikiid

def get_ent_name_from_wikiid(ent_wikiid):
    if ent_wikiid in e_id_name['ent_wikiid2name'].keys():
        ent_name = e_id_name['ent_wikiid2name'][ent_wikiid]
    else:
        ent_name = 0
    if not ent_name or not ent_wikiid:
        return 'NIL'
    return ent_name

if __name__ == '__main__':
    ent_name = ' <nada &amp; ada&quot; ,dada_xml '
    # preprocess_ent_name(ent_name)