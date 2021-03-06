# Generate p(e|m) index from Wikipedia
import sys

sys.path.append('/home/wenh/deep-el')
from data_gen.parse_wiki_dump_tools import extract_text_and_hyp
from entities.ent_name_id import get_ent_name_from_wikiid

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

with open(path, 'r', encoding='utf8') as f:
    for line in f:
        num_lines = num_lines + 1
        if num_lines % 5000000 == 0:
            print('Processed ' + str(num_lines) +
                  ' lines. Parsing errs= ' + str(parsing_errors) +
                  ' List ent errs= ' + str(list_ent_errors) +
                  ' diez errs = ' + str(diez_ent_errors) +
                  ' disambig errs= ' + str(disambiguation_ent_errors) +
                  ' . Num valid hyperlinks= ' + str(num_valid_hyperlinks))

        if not line.find('<doc id="') + 1:
            list_hyp, text, le_errs, p_errs, dis_errs, diez_errs = extract_text_and_hyp(line, False)
            parsing_errors = parsing_errors + p_errs
            list_ent_errors = list_ent_errors + le_errs
            disambiguation_ent_errors = disambiguation_ent_errors + dis_errs
            diez_ent_errors = diez_ent_errors + diez_errs
            for el in list_hyp:
                mention = el['mention']
                ent_wikiid = el['ent_wikiid']

                # A valid (entity,mention) pair
                num_valid_hyperlinks = num_valid_hyperlinks + 1

                if not wiki_e_m_counts.get(mention):
                    wiki_e_m_counts[mention] = {}

                if not wiki_e_m_counts[mention].get(ent_wikiid):
                    wiki_e_m_counts[mention][ent_wikiid] = 0
                wiki_e_m_counts[mention][ent_wikiid] = wiki_e_m_counts[mention][ent_wikiid] + 1

print('    Done computing Wikipedia p(e|m). Num valid hyperlinks = ' + str(num_valid_hyperlinks))

print('Now sorting and writing ..')
out_file = data_dir + 'generated/wikipedia_p_e_m.txt'
ouf = open(out_file, 'w')

for mention, lst in wiki_e_m_counts.items():
    tbl = []
    for ent_wikiid, freq in lst.items():
        t = {'ent_wikiid': ent_wikiid, 'freq': freq}
        tbl.append(t)
    tbl = sorted(tbl, key=lambda x: x["freq"], reverse=True)

    strs = ''
    total_freq = 0
    for el in tbl:
        strs = strs + str(el['ent_wikiid']) + ',' + str(el['freq'])
        strs = strs + ',' + get_ent_name_from_wikiid(el['ent_wikiid']).replace(' ', '_') + '\t'
        total_freq = total_freq + el['freq']
    ouf.write(mention + '\t' + str(total_freq) + '\t' + strs + '\n')
ouf.flush()
ouf.close()

print('    Done sorting and writing.')