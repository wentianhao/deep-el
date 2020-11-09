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

data_dir = '/home/wenh/'
rel_test_txtfilename = data_dir+'basic_data/relatedness/test.svm'
rel_test_t7filename = data_dir+'generated/relatedness_test.t7'
rel_validate_txtfilename = data_dir + 'basic_data/relatedness/validate.svm'
rel_validate_t7filename = data_dir + 'generated/relatedness_validate.t7'

def load_reltd_set(rel_t7filename, rel_txtfilename, set_type):
    print('==> Loading relatedness '+set_type)
    if not os.path.exists(rel_t7filename):
        print('  ---> t7 file NOT found. Loading relatedness '+set_type+' from txt file instead (slower).')
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
                    reltd[q][e1]=e1
                    cand = {}
                reltd[q][cand[e2]] = label


    return 'q'



if __name__ == '__main__':


    reltd_validate = load_reltd_set(rel_validate_t7filename, rel_validate_txtfilename, 'validate')
