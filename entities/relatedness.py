'''
The code in this file does two things:
a) extracts and puts the entity relatedness dataset in two maps (reltd_validate and
reltd_test). Provides functions to evaluate entity embeddings on this dataset
(Table 1 in our paper).
b) extracts all entities that appear in any of the ED (as mention candidates) or
entity relatedness datasets. These are placed in an object called rewtr that will
be used to restrict the set of entities for which we want to train entity embeddings
(done with the file entities/learn_e2v/learn_a.lua).
'''
import os
from entities.EX_wiki_words import *
import torch

data_dir = '/home/wenh/'
rel_test_txtfilename = data_dir + 'basic_data/relatedness/test.svm'
rel_test_t7filename = data_dir + 'generated/relatedness_test.t7'
rel_validate_txtfilename = data_dir + 'basic_data/relatedness/validate.svm'
rel_validate_t7filename = data_dir + 'generated/relatedness_validate.t7'
rewtr_t7filename = data_dir + 'generated/all_candidate_ents_ed_rltd_datasets_RLTD.t7'

'------------------------- Some function definitions -------------------'


# Loads the entity relatedness dataset (validation and test parts) in a map called reltd.
# Format: reltd = {query_id q -> (query_entity e1, entity_candidates cand) }
#         cand = {e2 -> label}, where label is binary, if the candidate entity is related to e1
def load_reltd_set(rel_t7filename, rel_txtfilename, set_type):
    print('==> Loading relatedness ' + str(set_type))
    if not os.path.exists(rel_t7filename):
        print('  ---> t7 file NOT found. Loading relatedness ' + str(set_type) + ' from txt file instead (slower).')
        reltd = {}
        with open(rel_txtfilename, 'r', encoding='utf8') as f:
            for line in f:
                parts = line.split(' ')
                label = int(parts[0])
                assert (label == 0 or label == 1)

                t = parts[1].split(':')
                q = int(t[1])

                i = 1
                while parts[i] != '#':
                    i = i + 1
                i = i + 1

                ents = parts[i].split('-')
                e1 = int(ents[0])
                e2 = int(ents[1])

                if not reltd.get(q):
                    reltd[q] = {}
                    reltd[q]['e1'] = e1
                    reltd[q]['cand'] = {}
                reltd[q]['cand'][e2] = label

        print('    Done loading relatedness ' + str(set_type) + '. Num queries = ' + str(len(reltd)) + '\n')
        print('Writing t7 File for future usage. Next time relatedness dataset will load faster!')
        torch.save(reltd, rel_t7filename)
        print(' Done saving.')

        return reltd
    else:
        print('---> from t7 file.')
        return torch.load(rel_t7filename)


# Extracts all entities in the relatedness set, either candidates or :
def extract_reltd_ents(reltd):
    reltd_ents_direct = {}
    for _, v in reltd.items():
        reltd_ents_direct[v['e1']] = 1
        for e2, _ in v['cand'].items():
            reltd_ents_direct[e2] = 1
    return reltd_ents_direct


if __name__ == '__main__':
    reltd_validate = load_reltd_set(rel_validate_t7filename, rel_validate_txtfilename, 'validate')
    reltd_test = load_reltd_set(rel_test_t7filename, rel_test_txtfilename, 'test')

    reltd_ents_direct_validate = extract_reltd_ents(reltd_validate)
    reltd_ents_direct_test = extract_reltd_ents(reltd_test)

    rewtr = {}
    print('==> Loading relatedness thid tensor')
    if not os.path.exists(rewtr_t7filename):
        print('  ---> t7 file NOT found. Loading reltd_ents_wikiid_to_rltdid from txt file instead (slower).')
        # Gather the restricted set of entities for which we train entity embeddings:
        rltd_all_ent_wikiids = {}
        # 1) From the relatedness dataset
        for ent_wikiid, _ in reltd_ents_direct_validate.items():
            rltd_all_ent_wikiids[ent_wikiid] = 1
        for ent_wikiid, _ in reltd_ents_direct_test.items():
            rltd_all_ent_wikiids[ent_wikiid] = 1
        # 1.1) From a small dataset (used for debugging / unit testing).
        for _, line in ent_lines_4EX.items():
            parts = line.split('\t')
            assert (len(parts) == 3)
            ent_wikiid = int(parts[0])
            assert ent_wikiid
            rltd_all_ent_wikiids[ent_wikiid] = 1
        #  2) From all ED datasets:
        files = {'aida_train.csv', 'aida_testA.csv', 'aida_testB.csv',
                 'wned-aquaint.csv', 'wned-msnbc.csv', 'wned-ace2004.csv',
                 'wned-clueweb.csv', 'wned-wikipedia.csv'}
        for file in files:
            with open(data_dir + 'generated/test_train_data/' + file, 'r', encoding='utf8') as f:
                for line in f:
                    parts = line.split('\t')
                    assert parts[5] == 'CANDIDATES'
                    assert parts[len(parts) - 1] == 'GT:'
                    if parts[6] != 'EMPTYCAND':
                        for i in range(6, len(parts) - 2):
                            p = parts[i].split(',')
                            ent_wikiid = int(p[0])
                            assert ent_wikiid
                            rltd_all_ent_wikiids[ent_wikiid] = 1

                        p = parts[len(parts) - 1].split(',')
                        if len(p) >= 2:
                            ent_wikiid = int(p[1])
                            assert ent_wikiid

        # Insert unk_ent_wikiid
        unk_ent_wikiid = 1
        rltd_all_ent_wikiids[unk_ent_wikiid] = 1

        # Sort all wikiids
        sorted_rltd_all_ent_wikiids = []
        for ent_wikiid, _ in rltd_all_ent_wikiids.items():
            sorted_rltd_all_ent_wikiids.append(ent_wikiid)
        sorted_rltd_all_ent_wikiids.sort()

        reltd_ents_wikiid_to_rltdid = {}
        for rltd_id, wikiid in enumerate(sorted_rltd_all_ent_wikiids):
            reltd_ents_wikiid_to_rltdid[wikiid] = rltd_id


        rewtr['reltd_ents_wikiid_to_rltdid'] = reltd_ents_wikiid_to_rltdid
        rewtr['reltd_ents_rltdid_to_wikiid'] = sorted_rltd_all_ent_wikiids
        rewtr['num_rltd_ents'] = len(sorted_rltd_all_ent_wikiids)

        print('Writing reltd_ents_wikiid_to_rltdid to t7 File for future usage.')
        torch.save(rewtr, rewtr_t7filename)
        print('    Done saving.')
    else:
        print('  ---> from t7 file.')
        rewtr = torch.load(rewtr_t7filename)

    print('    Done loading relatedness sets. Num queries test = ' + str(len(reltd_test)) +
          '. Num queries valid = ' + str(len(reltd_validate)) +
          '. Total num ents restricted set = ' + str(rewtr['num_rltd_ents']))
