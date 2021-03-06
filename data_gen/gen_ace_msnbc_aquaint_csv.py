'''
Generate test data from the ACE/MSNBC/AQUAINT datasets by keeping the context and
entity candidates for each annotated mention

Format:
doc_name \t doc_name \t mention \t left_ctxt \t right_ctxt \t CANDIDATES \t [ent_wikiid,p_e_m,ent_name]+ \t GT: \t pos,ent_wikiid,p_e_m,ent_name

Stats:
-- cat wned-ace2004.csv |  wc -l
-- 257
-- cat wned-ace2004.csv |  grep -P 'GT:\t-1' | wc -l
-- 20
-- cat wned-ace2004.csv | grep -P 'GT:\t1,' | wc -l
-- 217
-- cat wned-aquaint.csv |  wc -l
-- 727
-- cat wned-aquaint.csv |  grep -P 'GT:\t-1' | wc -l
-- 33
-- cat wned-aquaint.csv | grep -P 'GT:\t1,' | wc -l
-- 604
-- cat wned-msnbc.csv  | wc -l
-- 656
-- cat wned-msnbc.csv |  grep -P 'GT:\t-1' | wc -l
-- 22
-- cat wned-msnbc.csv | grep -P 'GT:\t1,' | wc -l
-- 496
'''
import sys
sys.path.append('/home/wenh/deep-el')
from data_gen.yago_crosswikis_wiki import *
from entities.ent_name_id import *


def gen_test_ace(dataset):
    print('\nGenerating test data from ' + dataset + ' set ')

    path = data_dir + 'basic_data/test_datasets/wned-datasets/' + dataset + '/'
    out_file = data_dir + 'generated/test_train_data/wned-' + dataset + '.csv'
    ouf = open(out_file, 'w')

    annotations = path + dataset + '.xml'

    num_nonexistent_ent_id = 0
    num_correct_ents = 0
    cur_doc_text = ''
    cur_doc_name = ''
    with open(annotations, 'r', encoding='utf8') as f:
        line = f.readline()
        while line:
            if not line.find('document docName=\"') + 1:
                if line.find('<annotation>') + 1:
                    line = f.readline()
                    x = line.find('<mention>')
                    y = x + len('<mention>>') - 1
                    z = line.find('</mention>')
                    t = z + len('</mention>') - 1
                    cur_mention = line[y:z]
                    print(cur_mention)
                    cur_mention = cur_mention.replace('&amp;', '&')

                    # entity title
                    line = f.readline()
                    x = line.find('<wikiName>')
                    y = x + len('<wikiName>')
                    z = line.find('</wikiName>')
                    t = z + len('</wikiName>')
                    cur_ent_title = ''
                    if not line.find('<wikiName/>') + 1:
                        cur_ent_title = line[y:z]

                    # offset
                    line = f.readline()
                    x = line.find('<offset>')
                    y = x + len('<offset>')
                    z = line.find('</offset>')
                    t = z + len('</offset>')
                    offset = int(line[y:z])

                    line = f.readline()
                    x = line.find('<length>')
                    y = x + len('<length>')
                    z = line.find('</length>')
                    t = z + len('</length>')
                    length = int(line[y:z])
                    length = len(cur_mention)

                    line = f.readline()
                    if line.find('<entity/>') + 1:
                        line = f.readline()

                    assert line.find('</annotation>')

                    offset = max(0, offset - 10)
                    while (cur_doc_text[offset:offset + length] != cur_mention):
                        # print(cur_mention + ' ---> ' + cur_doc_text[offset:offset + length])
                        offset = offset + 1

                    cur_mention = preprocess_mention(cur_mention)

                    if cur_ent_title != 'NIL' and cur_ent_title != '' and len(cur_ent_title) > 0:
                        cur_ent_wikiid = get_ent_wikiid_from_name(cur_ent_title, False)
                        if cur_ent_wikiid == unk_ent_wikiid:
                            num_nonexistent_ent_id = num_nonexistent_ent_id + 1
                            print(cur_ent_title)
                        else:
                            num_correct_ents = num_correct_ents + 1
                        assert len(cur_mention) > 0

                        strs = cur_doc_name + '\t' + cur_doc_name + '\t' + cur_mention + '\t'

                        left_words = split_in_words(cur_doc_text[0:offset - 1])
                        num_left_words = len(left_words)
                        left_ctxt = []
                        for i in range(max(0, num_left_words - 100), num_left_words):
                            left_ctxt.append(left_words[i])
                        if len(left_ctxt) == 0:
                            left_ctxt.append('EMPTYCTXT')
                        left_ctxts = ''
                        for l_ctxt in left_ctxt:
                            left_ctxts = left_ctxts + l_ctxt + ' '
                        strs = strs + left_ctxts + '\t'

                        right_words = split_in_words(cur_doc_text[offset + length-1:])
                        num_right_words = len(right_words)
                        right_ctxt = []
                        for i in range(0, min(num_right_words , 100)):
                            right_ctxt.append(right_words[i])
                        if len(right_ctxt) == 0:
                            right_ctxt.append('EMPTYCTXT')
                        right_ctxts = ''
                        for r_ctxt in right_ctxt:
                            right_ctxts = right_ctxts + r_ctxt + ' '
                        strs = strs + right_ctxts + '\tCANDIDATES\t'

                        # Entity candidates from p(e|m) dictionary
                        if ent_p_e_m_index.get(cur_mention) and len(ent_p_e_m_index[cur_mention]) > 0:
                            sorted_cand = []
                            for ent_wikiid, p in ent_p_e_m_index[cur_mention].items():
                                cand = {'ent_wikiid': ent_wikiid, 'p': p}
                                sorted_cand.append(cand)
                            sorted_cand = sorted(sorted_cand, key=lambda x: x["p"], reverse=True)

                            candidates = []
                            gt_pos = -1
                            for pos,e in enumerate(sorted_cand):
                                if pos <= 99:
                                    candidates.append(str(e['ent_wikiid']) + ',' + "{:.3f}".format(
                                        e['p']) + ',' + get_ent_name_from_wikiid(e['ent_wikiid']))
                                    if e['ent_wikiid'] == cur_ent_wikiid:
                                        gt_pos = pos
                                else:
                                    break
                            total_cand = ''
                            for candidate in candidates:
                                total_cand = total_cand + candidate + '\t'
                            strs = strs + total_cand + 'GT:\t'

                            if gt_pos >= 0:
                                ouf.write(strs + str(gt_pos) + ',' + candidates[gt_pos] + '\n')
                            else:
                                if cur_ent_wikiid != unk_ent_wikiid:
                                    ouf.write(strs + '-1,' + str(cur_ent_wikiid) + ',' + cur_ent_title + '\n')
                                else:
                                    ouf.write(strs + '-1\n')
                        else:
                            if cur_ent_wikiid != unk_ent_wikiid:
                                ouf.write(
                                    strs + 'EMPTYCAND\tGT:\t-1,' + str(cur_ent_wikiid) + ',' + cur_ent_title + '\n')
                            else:
                                ouf.write(strs + 'EMPTYCAND\tGT:\t-1\n')
            else:
                x = line.find('document docName=\"')
                y = x + len('document docName=\"')
                z = line.find('\">')
                t = z + len('\">') - 1
                cur_doc_name = line[y:z]
                cur_doc_name = cur_doc_name.replace('&amp;', '&')
                # 通过docName读取无标签文本
                with open(path + 'RawText/' + cur_doc_name, 'r', encoding='utf8') as fd:
                    for cur_line in fd:
                        cur_doc_text = cur_doc_text + cur_line
                    cur_doc_text = cur_doc_text.replace('&amp;', '&')

            line = f.readline()
    ouf.flush()
    ouf.close()

    print('Done ' + dataset + '.')
    print('num_nonexistent_ent_id = ' + str(num_nonexistent_ent_id) + '; num_correct_ents = ' + str(num_correct_ents))


if __name__ == '__main__':
    gen_test_ace('wikipedia')
    print('Done wikipedia !')
    gen_test_ace('clueweb')
    print('Done clueweb !')
    gen_test_ace('ace2004')
    print('Done ace2004 !')
    gen_test_ace('msnbc')
    print('Done msnbc !')
    gen_test_ace('aquaint')
    print('Done Gen ace msnbc aquaint !')
