# Utility functions to extract the text and hyperlinks from each page in the Wikipedia corpus.
# 提取文本和超链接

import Utils.utils
import entities.ent_name_id as eni


def extract_text_and_hyp(line,mark_mentions):
    list_hyp = {}   # (mention,entities)
    text = ''
    list_ent_errors = 0
    parsing_errors = 0
    disambiguation_ent_errors = 0
    diez_ent_errors = 0

    end_end_hyp = 0
    begin_end_hyp = 0
    begin_start_hyp = line.find('<a href="')
    end_start_hyp = begin_end_hyp + len('<a href="') - 1
    num_mentions = 0

    while begin_start_hyp :
        text = text + line[end_end_hyp:begin_start_hyp]

        next_quotes = line.find('">',end_start_hyp + 1)
        end_quotes = next_quotes + len('">') -1
        if next_quotes + 1:
            ent_name = line[end_start_hyp:next_quotes]
            if begin_end_hyp:
                mention = line[end_quotes:begin_end_hyp]
                mention_maker = False
                good_mention = True
                good_mention = good_mention and (not mention.find('Wikipedia'))
                good_mention = good_mention and (not mention.find('wikipedia'))
                good_mention = good_mention and (len(mention) >= 1)

                if good_mention:
                    i = ent_name.find('wikt:')
                    if i== 1:
                        ent_name = ent_name.sub(6)
                    ent_name = eni.preprocess_ent_name(ent_name)

                    i = ent_name.find('List of ') + 1
                    if (not i) or(i !=1):
                        if ent_name.find('#')+1:
                            diez_ent_errors = diez_ent_errors +1
                        else:
                            ent_wikiId = eni.get_ent_wikiid_from_name(ent_name,True)



    return