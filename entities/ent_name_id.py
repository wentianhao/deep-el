import Utils.utils as tl
import data_gen.wiki_redirects_index as wri
import data_gen.wiki_disambiguation_pages_index as wdpi
import torch
import os
import entities.relatedness

rltd_only = False
enttype = 'RLTD'
if enttype and enttype!='ALL':
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

        # if not wdpi.wiki_disambiguation_index[ent_wikiid]:
        #     if not rltd_only





def preprocess_ent_name(ent_name):
    ent_name = tl.trim1(ent_name)
    ent_name = ent_name.replace('&amp;', '&')
    ent_name = ent_name.replace('&quot;', '"')
    ent_name = ent_name.replace('_', ' ')
    ent_name= tl.first_letter_to_uppercase(ent_name)
    if wri.get_redirected_ent_title:
        ent_name = wri.get_redirected_ent_title(ent_name)
    return ent_name

def get_ent_wikiid_from_name(ent_name,not_verbose):
    verbose = (not not_verbose)
    ent_name = preprocess_ent_name(ent_name)
    ent_wikiid = e_id_name

if __name__ == '__main__':
    ent_name = ' <nada &amp; ada&quot; ,dada_xml '
    # preprocess_ent_name(ent_name)