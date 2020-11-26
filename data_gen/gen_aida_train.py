# Generate train data from the AIDA dataset by keeping the context and
# entity candidates for each annotated mention
#
# Format:
# doc_name \t doc_name \t mention \t left_ctxt \t right_ctxt \t CANDIDATES \t [ent_wikiid,p_e_m,ent_name]+ \t GT: \t pos,ent_wikiid,p_e_m,ent_name
import sys
sys.path.append('/home/wenh/deep-el')
from data_gen.wiki_redirects_index import *
from data_gen.yago_crosswikis_wiki import *
from Utils.utils import *
from entities.ent_name_id import *

print('\nGenerating train data from AIDA set ')

out_file = data_dir+'generated/test_train_data/aida_train.csv'
ouf = open(out_file,'w')

num_nme = 0
num_nonexistent_ent_title = 0
num_nonexistent_ent_id = 0
num_nonexistent_both = 0
num_correct_ents = 0
num_total_ents = 0

cur_words_num = 0
cur_words = {}
cur_mentions = {}
cur_mentions_num = 0

cur_doc_name = ''

def write_results():
    # Write results
    if cur_doc_name != '':
        header = cur_doc_name + '\t' + cur_doc_name + '\t'
        for _,hyp in cur_mentions.items():
            assert len(hyp['mention']) > 0
            mention = hyp['mention']
            strs = header + hyp['mention']+'\t'

            left_ctxt = []
            for i in range(max(0,hyp['start_off']-100),hyp['start_off']-1):
                left_ctxt.append(cur_words[i-1])
            if len(left_ctxt) == 0:
                left_ctxt.append('EMPTYCTXT')
            l_ctxts = ''
            for l_ctxt in left_ctxt:
                l_ctxts = l_ctxts + l_ctxt + ' '
            strs = strs + l_ctxts + '\t'

            right_ctxt = []
            for i in range(hyp['end_off'],min(cur_words_num,hyp['end_off']+99)):
                right_ctxt.append(cur_words[i])
            if len(right_ctxt) == 0:
                right_ctxt.append('EMPTYCTXT')
            r_ctxts = ''
            for r_ctxt in right_ctxt:
                r_ctxts = r_ctxts + r_ctxt + ' '
            strs = strs + r_ctxts + '\tCANDIDATES\t'

            # Entity candidates from p(e|m) dictionary
            if mention in ent_p_e_m_index.keys():
                if len(ent_p_e_m_index[mention]) >0:
                    sorted_cand = []
                    for ent_wikiid,p in ent_p_e_m_index[mention].items():
                        cand = {}
                        cand['ent_wikiid'] = ent_wikiid
                        cand['p'] = p
                        sorted_cand.append(cand)
                    sorted_cand = sorted(sorted_cand, key=lambda x: x["p"], reverse=True)

                    candidates = []
                    gt_pos = -1
                    pos = -1
                    for e in sorted_cand:
                        pos = pos + 1
                        if pos < 100:
                            candidates.append(str(e['ent_wikiid'])+','+"{:.3f}".format(e['p'])+','+get_ent_name_from_wikiid(e['ent_wikiid']))
                            if e['ent_wikiid'] == hyp['ent_wikiid']:
                                gt_pos = pos
                        else:
                            break
                    total_cand = ''
                    for candidate in candidates:
                        total_cand = total_cand + candidate + '\t'
                    strs = strs + total_cand + 'GT:\t'

                    if gt_pos > 0:
                        ouf.write(strs+str(gt_pos)+','+candidates[gt_pos]+'\n')

with open(data_dir+'basic_data/test_datasets/AIDA/aida_train.txt','r',encoding='utf8') as f:
    for line in f:
        if not line.find('-DOCSTART-') +1:
            parts = line.split('\t')
            num_parts = len(parts)
            assert num_parts == 0 or num_parts ==1 or num_parts ==4 or num_parts ==7 or num_parts ==6
            if num_parts > 0:
                if num_parts == 4 and parts[1] == 'B':
                    num_nme = num_nme + 1

                if (num_parts ==7 or num_parts ==6) and parts[1] == 'B':
                    # Find current mention. A few hacks here.
                    cur_mention = preprocess_mention(parts[2])

                    x = parts[4].find('/wiki/')
                    y = x + len('/wiki/')
                    cur_ent_title = parts[4][y:]
                    cur_ent_wikiid = int(parts[5])
                    index_ent_title = get_ent_name_from_wikiid(cur_ent_wikiid)
                    index_ent_wikiid = get_ent_wikiid_from_name(cur_ent_title)

                    final_ent_wikiid = index_ent_wikiid
                    if final_ent_wikiid == unk_ent_wikiid:
                        final_ent_wikiid = cur_ent_wikiid

                    if index_ent_title == cur_ent_title and cur_ent_wikiid == index_ent_wikiid:
                        num_correct_ents = num_correct_ents + 1
                    elif index_ent_title != cur_ent_title and cur_ent_wikiid != index_ent_wikiid:
                        num_nonexistent_both = num_nonexistent_both + 1
                    elif index_ent_title != cur_ent_title:
                        assert cur_ent_wikiid == index_ent_wikiid
                        num_nonexistent_ent_title = num_nonexistent_ent_title + 1
                    else:
                        assert index_ent_title == cur_ent_title
                        assert cur_ent_wikiid != index_ent_wikiid
                        num_nonexistent_ent_id = num_nonexistent_ent_id + 1

                    num_total_ents = num_total_ents + 1 # keep even incorrect links

                    cur_mentions_num = cur_mentions_num + 1
                    cur_mentions[cur_mentions_num] = {}
                    cur_mentions[cur_mentions_num]['mention'] = cur_mention
                    cur_mentions[cur_mentions_num]['ent_wikiid'] = final_ent_wikiid
                    cur_mentions[cur_mentions_num]['start_off'] = cur_words_num + 1
                    cur_mentions[cur_mentions_num]['end_off'] = cur_words_num + len(parts[2].split(' '))

                words_on_this_line = split_in_words(parts[0])
                for w in words_on_this_line:
                    cur_words.append(modify_uppercase_phrase(w))
                    cur_words_num = cur_words_num + 1
        else:
            assert line.find('-DOCSTART-')+1
            write_results()

            cur_doc_name = line[12:]

            cur_words = []
            cur_words_num = 0
            cur_mentions = {}
            cur_mentions_num = 0

write_results()
ouf.flush()
ouf.close()

print('    Done AIDA.')
print('num_nme = ' + str(num_nme) + '; num_nonexistent_ent_title = ' + str(num_nonexistent_ent_title))
print('num_nonexistent_ent_id = ' + str(num_nonexistent_ent_id) + '; num_nonexistent_both = ' + str(num_nonexistent_both))
print('num_correct_ents = ' + str(num_correct_ents) + '; num_total_ents = ' + str(num_total_ents))
