# loads the merged p(e|m) index

ent_p_e_m_index = {}

mention_lower_to_one_upper = {}

mention_total_freq = {}

data_dir = '/home/wenh/'
crosswikis_textfilename = data_dir + 'generated/crosswikis_wikipedia_p_e_m.txt'
print('==> Loading crosswikis_wikipedia from file :' + crosswikis_textfilename)

num_lines = 0

with open(crosswikis_textfilename,'r',encoding='utf8') as f:
    for line in f:
        num_lines = num_lines + 1
        if num_lines % 200000 == 0:
            print('Processed ' + str(num_lines) + ' lines. ')

        parts = line.split('\t')
        mention = parts[0]

        total = int(parts[1])
        assert total
        if total >= 1:
            ent_p_e_m_index[mention] = {}
            mention_lower_to_one_upper[mention.lower()] = mention
            mention_total_freq[mention] = total
            num_parts = len(parts)
            for i in range(2,num_parts-1):
                ent_str = parts[i].split(',')
                ent_wikiid = int(ent_str[0])
                assert ent_wikiid
                freq = int(ent_str[1])
                assert freq
                ent_p_e_m_index[mention][ent_wikiid] = freq / (total + 0.0) # not sorted

yago_textfilename = data_dir + 'generated/yago_p_e_m.txt'
print('==> Loading yago index from file ' + yago_textfilename)

num_lines = 0
with open(yago_textfilename,'r',encoding='utf8') as f:
    for line in f:
        num_lines = num_lines + 1
        if num_lines % 2000000 == 0:
            print('Processed ' + num_lines + ' lines. ')

        parts = line.split('\t')
        mention = parts[0]
        total = int(parts[1])
        assert total

        if total >= 1:
            mention_lower_to_one_upper[mention.lower()] = mention
            if mention not in mention_total_freq.keys():
                mention_total_freq[mention] = total
            else:
                mention_total_freq[mention] = total + mention_total_freq[mention]

            yago_ment_ent_idx = {}
            num_parts = len(parts)
            for i in range(2,num_parts-1):
                ent_str = parts[i].split(',')
                ent_wikiid = int(ent_str[0])
                freq = 1
                assert ent_wikiid
                yago_ment_ent_idx[ent_wikiid] = freq / (total+0.0)

            if mention not in ent_p_e_m_index.keys():
                ent_p_e_m_index[mention] = yago_ment_ent_idx
            else:
                for ent_wikiid,prob in yago_ment_ent_idx.items():
                    if ent_wikiid not in ent_p_e_m_index[mention].keys():
                        ent_p_e_m_index[mention][ent_wikiid] = 0.0
                    ent_p_e_m_index[mention][ent_wikiid] = min(1.0,ent_p_e_m_index[mention][ent_wikiid]+prob)

assert(ent_p_e_m_index['Dejan Koturovic'] and ent_p_e_m_index['Jose Luis Caminero'])

#  Function used to preprocess a given mention such that it has higher
#  chance to have at least one valid entry in the p(e|m) index.

def preprocess_mention(m):
    assert ent_p_e_m_index and mention_total_freq
    cur_m = ''