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
import torch


data_dir = '/home/wenh/'

def gen_test_ace(dataset):

    print('\nGenerating test data from ' + dataset + ' set ')

    path = data_dir + 'basic_data/test_datasets/wned-datasets/'+dataset+'/'
    out_file = data_dir + 'generated/test_train_data/wned-'+dataset+'.csv'
    ouf = open(out_file,'w')

    annotations = path + dataset+'.xml'

    num_nonexistent_ent_id = 0
    num_correct_ents = 0
    cur_doc_text = ''
    cur_doc_name = ''
    with open(annotations,'r',encoding='utf8') as f:
        line = f.readline()
        while line:
            if not line.find('document docName=\"')+1:
                if line.find('<annotation>') + 1:
                    line = f.readline()
                    x = line.find('<mention>')
                    y = x + len('<mention>>') - 1
                    z = line.find('</mention>')
                    t = z + len('</mention>') - 1
                    cur_mention = line[y:z]
                    print(cur_mention)
                    cur_mention = cur_mention.replace('&amp;','&')

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
                    offset = 1 + int(line[y:z])

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

                    offset = max(0,offset-9)
                    while (cur_doc_text[offset:offset+length-1] != cur_mention):
                        print(cur_mention + ' ---> ' + cur_doc_text[offset:offset + length - 1])
                        offset = offset + 1

                    cur_mention = preprocess_mention(cur_mention)



            else:
                x = line.find('document docName=\"')
                y = x + len('document docName=\"')
                z = line.find('\">')
                t = z + len('\">') - 1
                cur_doc_name = line[y:z]
                cur_doc_name = cur_doc_name.replace('&amp;','&')
                # 通过docName读取无标签文本
                with open(path+'RawText/'+cur_doc_name,'r',encoding='utf8') as fd:
                    for cur_line in fd:
                        cur_doc_text = cur_doc_text + cur_line
                    cur_doc_text = cur_doc_text.replace('&amp;','&')

            line = f.readline()


if __name__ == '__main__':
    gen_test_ace('wikipedia')

