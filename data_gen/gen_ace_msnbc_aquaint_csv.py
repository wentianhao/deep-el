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
import data_gen.wiki_redirects_index
import Utils.utils

root_data_dir = '/home/wenh/'

def gen_test_ace(dataset):

    print('\nGenerating test data from ' + dataset + ' set ')

    path = root_data_dir + 'basic_data/test_datasets/wned-datasets/'
