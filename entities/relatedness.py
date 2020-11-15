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
import Utils.utils
import entities.EX_wiki_words as eww
import torch

data_dir = '/home/wenh/'
rel_test_txtfilename = data_dir+'basic_data/relatedness/test.svm'
rel_test_t7filename = data_dir+'generated/relatedness_test.t7'
rel_validate_txtfilename = data_dir + 'basic_data/relatedness/validate.svm'
rel_validate_t7filename = data_dir + 'generated/relatedness_validate.t7'
rewtr_t7filename = data_dir + 'generated/all_candidate_ents_ed_rltd_datasets_RLTD.t7'

def load_reltd_set(rel_t7filename, rel_txtfilename, set_type):
    print('==> Loading relatedness '+str(set_type))
    if not os.path.exists(rel_t7filename):
        print('  ---> t7 file NOT found. Loading relatedness '+str(set_type)+' from txt file instead (slower).')
        reltd = {}
        with open(rel_txtfilename,'r',encoding='utf8') as f:
            for line in f:
                parts = line.split(' ')
                label = int(parts[0])
                assert (label == 0 or label == 1)

                t = parts[1].split(':')
                q = int(t[1])

                i = 1
                while parts[i] != '#':
                    i = i + 1
                i = i +1

                ents = parts[i].split('-')
                e1 = int(ents[0])
                e2 = int(ents[1])

                if not reltd.get(q):
                    reltd[q]={}
                    reltd[q]['e1']=e1
                    cand = {}
                cand[e2] = label
                reltd[q]['cand'] = cand

        print('    Done loading relatedness '+ str(set_type) + '. Num queries = '+str(len(reltd))+'\n')
        print('Writing t7 File for future usage. Next time relatedness dataset will load faster!')
        torch.save(reltd,rel_t7filename)
        print(' Done saving.')

        return reltd
    else:
        print('---> from t7 file.')
        return torch.load(rel_t7filename)

def extract_reltd_ents(reltd):
    reltd_ents_direct = {}
    for _,v in reltd.items():
        reltd_ents_direct[v.get('e1')] = 1
        for e2,_ in v['cand'].items():
            reltd_ents_direct[e2] = 1
    return reltd_ents_direct


if __name__ == '__main__':
    reltd_validate = load_reltd_set(rel_validate_t7filename, rel_validate_txtfilename, 'validate')
    reltd_test = load_reltd_set(rel_test_t7filename,rel_test_txtfilename,'test')

    reltd_ents_direct_validate = extract_reltd_ents(reltd_validate)
    reltd_ents_direct_test = extract_reltd_ents(reltd_test)

    print('==> Loading relatedness thid tensor')
    if not os.path.exists(rewtr_t7filename):
        print('  ---> t7 file NOT found. Loading reltd_ents_wikiid_to_rltdid from txt file instead (slower).')
        # Gather the restricted set of entities for which we train entity embeddings:
        rltd_all_ent_wikiids = {}
        # 1) From the relatedness dataset
        for ent_wikiid,_ in reltd_ents_direct_validate.items():
            rltd_all_ent_wikiids[ent_wikiid] = 1
        for ent_wikiid,_ in reltd_ents_direct_test.items():
            rltd_all_ent_wikiids[ent_wikiid] = 1
        # 1.1) From a small dataset (used for debugging / unit testing).
        for _,line in eww.ent_lines_4EX.items():
            parts = line.split('\t')
            assert (len(parts) == 3)
            ent_wikiid = int(parts[0])
            assert ent_wikiid
            rltd_all_ent_wikiids[ent_wikiid] = 1
        #  2) From all ED datasets:
    #     files = {'aida_train.csv', 'aida_testA.csv', 'aida_testB.csv',
    # 'wned-aquaint.csv', 'wned-msnbc.csv', 'wned-ace2004.csv',
    # 'wned-clueweb.csv', 'wned-wikipedia.csv'}
    #     for file in files:
    #         with open(data_dir+'generated/test_train_data/'+file,'r',encoding='utf8') as f :
    #             for line in f :
    #                 parts = line.split('\t')
    #                 assert parts[5] == 'CANDIDATES'
    #                 assert parts[len(parts) - 1] == 'GT:'
    #                 if parts[6] != 'EMPTYCAND':
    #                     for i in range(6,len(parts)-2):
    #                         p = parts[i].split(',')
    #                         ent_wikiid = int(p[0])
    #                         assert ent_wikiid
    #                         rltd_all_ent_wikiids[ent_wikiid] = 1
    #
    #                     p = parts[len(parts)-1].split(',')
    #                     if len(p)>=2 :
    #                         ent_wikiid = int(p[1])
    #                         assert ent_wikiid
