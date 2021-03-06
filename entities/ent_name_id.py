'''
Each entity has:
a) a Wikipedia URL refferred as 'name' here
b) a Wikipedia ID refferred as 'ent_wikiid' or 'wikiid' here
c) an ID that will be used in the entity embeddings lookup table. Referred as 'ent_thid' or 'thid' there
'''

from Utils.utils import *
from data_gen.wiki_redirects_index import *
from entities.relatedness import *
import torch
import os

unk_ent_wikiid = 1
rltd_only = False
# ent_type = 'RLTD'
# if ent_type and ent_type != 'ALL':
#     rltd_only = True

# Unk entity wikiid
unk_ent_wikiid = 1

entity_wiki_txtfilename = '/home/wenh/' + 'basic_data/wiki_name_id_map.txt'
entity_wiki_t7filename = '/home/wenh/' + 'generated/ent_name_id_map.t7'
if rltd_only:
    entity_wiki_t7filename = '/home/wenh/' + 'generated/ent_name_id_map_RLTD.t7'

print('==> Loading entities wikiid - name map')

e_id_name = 0

if os.path.exists(entity_wiki_t7filename):
    print(' ---> from t7 file: ' + entity_wiki_t7filename)
    e_id_name = torch.load(entity_wiki_t7filename)
else:
    print('  ---> t7 file NOT found. Loading from disk (slower). Out f = ' + entity_wiki_t7filename)
    from data_gen.wiki_disambiguation_pages_index import *
    print('    Still loading entities wikiid - name map ...')

    e_id_name = {}

    # map for entity name to entity wiki id
    e_id_name['ent_wikiid2name'] = {}
    e_id_name['ent_name2wikiid'] = {}

    # map for entity wiki id to tensor id. Size = 4.4M
    if not rltd_only:
        e_id_name['ent_wikiid2thid'] = {}
        e_id_name['ent_thid2wikiid'] = {}

    cnt = 0
    cnt_freq = 0
    with open(entity_wiki_txtfilename, 'r', encoding='utf8') as f:
        for line in f:
            parts = line.split('\t')
            ent_name = parts[0]
            ent_wikiid = int(parts[1])

            if not wiki_disambiguation_index.get(ent_wikiid):
                if not rltd_only or rewtr['reltd_ents_wikiid_to_rltdid'][ent_wikiid]:
                    e_id_name['ent_wikiid2name'][ent_wikiid] = ent_name
                    e_id_name['ent_name2wikiid'][ent_name] = ent_wikiid
                if not rltd_only:
                    cnt = cnt + 1
                    e_id_name['ent_wikiid2thid'][ent_wikiid] = cnt
                    e_id_name['ent_thid2wikiid'][cnt] = ent_wikiid
    if not rltd_only:
        cnt = cnt + 1
        e_id_name['ent_wikiid2thid'][unk_ent_wikiid] = cnt
        e_id_name['ent_thid2wikiid'][cnt] = unk_ent_wikiid

    e_id_name['ent_wikiid2name'][unk_ent_wikiid] = 'UNK_ENT'
    e_id_name['ent_name2wikiid']['UNK_ENT'] = unk_ent_wikiid

    torch.save(e_id_name, entity_wiki_t7filename)

if not rltd_only:
    unk_ent_thid = e_id_name['ent_wikiid2thid'][unk_ent_wikiid]
else:
    unk_ent_thid = rewtr['reltd_ents_wikiid_to_rltdid'][unk_ent_wikiid]  # 之后再写


def preprocess_ent_name(ent_name):
    ent_name = trim1(ent_name)
    ent_name = ent_name.replace('&amp;', '&')
    ent_name = ent_name.replace('&quot;', '"')
    ent_name = ent_name.replace('_', ' ')
    if ent_name == ' ' or ent_name == '':
        return ent_name
    ent_name = first_letter_to_uppercase(ent_name)
    if get_redirected_ent_title:
        ent_name = get_redirected_ent_title(ent_name)
    return ent_name


def get_ent_wikiid_from_name(ent_name, not_verbose):
    verbose = (not not_verbose)
    ent_name = preprocess_ent_name(ent_name)
    ent_wikiid = e_id_name['ent_name2wikiid'].get(ent_name)
    if not ent_wikiid or not ent_name:
        if verbose:
            print('Entity ' + ent_name + ' not found. Redirects file needs to be loaded for better performance.')
        return unk_ent_wikiid
    return ent_wikiid


def get_ent_name_from_wikiid(ent_wikiid):
    ent_name = e_id_name['ent_wikiid2name'].get(ent_wikiid)
    if not ent_name or not ent_wikiid:
        return 'NIL'
    return ent_name


def is_valid_ent(ent_wikiid):
    if e_id_name['ent_wikiid2name'].get(ent_wikiid):
        return True
    return False

def get_total_num_ents():
    if rltd_only:
        assert len(rewtr['reltd_ents_wikiid_to_rltdid'])==rewtr['num_rltd_ents']
        return len(rewtr['reltd_ents_wikiid_to_rltdid'])
    else:
        return len(e_id_name['ent_thid2wikiid'])

def get_map_all_valid_ents():
    m = {}
    for ent_wikiid,_ in e_id_name['ent_wikiid2name'].items():
        m[ent_wikiid] = 1
    return m

print('    Done loading entity name - wikiid. Size thid index = ' + str(get_total_num_ents()))
if __name__ == '__main__':
    ent_name = ' <nada &amp; ada&quot; ,dada_xml '
    # preprocess_ent_name(ent_name)
