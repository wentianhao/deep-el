import data_gen.parse_wiki_dump_tools as pkd

data_dir = '/home/wenh/'
num_lines = 0
parsing_errors = 0
list_ent_errors = 0
diez_ent_errors = 0
disambiguation_ent_errors = 0
num_valid_hyperlinks = 0

wiki_e_m_counts = {}
path = data_dir + 'basic_data/textWithAnchorsFromAllWikipedia2014Feb.txt'

print('\n Computing Wikipedia p_e_m')

with open(path,'r',encoding='utf8') as f:
    for line in f:
        num_lines = num_lines + 1
        if num_lines % 500000 == 0:
            print('Processed '+ str(num_lines)+
                  ' lines. Parsing errs= '+str(parsing_errors)+
                  ' List ent errs= '+str(list_ent_errors)+
                  ' diez errs = '+ str(diez_ent_errors)+
                  ' disambig errs= '+ str(disambiguation_ent_errors)+
                  ' . Num valid hyperlinks= '+str(num_valid_hyperlinks))

        if not line.find('<doc id="'):
            list_hyp, text, le_errs, p_errs, dis_errs, diez_errs = pkd.extract_text_and_hyp(line, false)