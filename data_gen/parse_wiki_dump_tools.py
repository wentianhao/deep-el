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
    begin_start_hyp = line.find('<a href="')+1
    end_start_hyp = begin_end_hyp + len('<a href="') - 1
    num_mentions = 0

    unk_ent_wikiid = 1

    while begin_start_hyp :
        text = text + line[end_end_hyp:begin_start_hyp-1]
        next_quotes = line.find('">',end_start_hyp + 1)
        end_quotes = next_quotes + len('">') -1
        if next_quotes + 1:
            ent_name = line[end_start_hyp+1:next_quotes]
            begin_end_hyp = line.find('</a>',end_quotes+1)
            end_end_hyp = begin_end_hyp + len('</a>')
            if begin_end_hyp:
                mention = line[end_quotes+1:begin_end_hyp]
                mention_maker = False
                good_mention = True
                good_mention = good_mention and (not mention.find('Wikipedia')+1)
                good_mention = good_mention and (not mention.find('wikipedia')+1)
                good_mention = good_mention and (len(mention) >= 1)

                if good_mention:
                    i = ent_name.find('wikt:')+1
                    if i== 1:
                        ent_name = ent_name.sub(6)
                    ent_name = eni.preprocess_ent_name(ent_name)

                    i = ent_name.find('List of ') + 1
                    if (not i) or(i !=1):
                        if ent_name.find('#')+1:
                            diez_ent_errors = diez_ent_errors +1
                        else:
                            ent_wikiId = eni.get_ent_wikiid_from_name(ent_name,True)
                            if ent_wikiId == unk_ent_wikiid:
                                disambiguation_ent_errors = disambiguation_ent_errors + 1
                            else:
                                # A valid (entity,mention) pair
                                num_mentions = num_mentions + 1
                                list_hyp['mention'] = mention
                                list_hyp['ent_wikiid'] = ent_wikiId
                                list_hyp['cnt'] = num_mentions
                                if mark_mentions:
                                    mark_mentions = True
                    else:
                        list_ent_errors = list_ent_errors + 1
                if not mention_maker:
                    text = text + ' ' + mention + ' '
                else:
                    text = text + 'MMSTART' + str(num_mentions) +' '+str(mention)+'MMEND'+str(num_mentions)+' '
            else:
                parsing_errors = parsing_errors + 1
                begin_start_hyp = 0

            if begin_start_hyp:
                begin_start_hyp = line.find('<a href="')
                end_start_hyp = begin_start_hyp + len('<a href="')

            if end_end_hyp:
                text = text + line[end_end_hyp:]
            else:
                if not mark_mentions:
                    text = line
                else:
                    text = ''
                    list_hyp = {}

    return list_hyp,text,list_ent_errors,parsing_errors,disambiguation_ent_errors,diez_ent_errors

# Unit tests
if __name__ == '__main__':
    print('\n Unit tests:')
    test_line_1 = '<a href="Anarchism">Anarchism</a> is a <a href="political philosophy">political philosophy</a> that advocates<a href="stateless society">stateless societies</a>often defined as <a href="self-governance">self-governed</a> voluntary institutions, but that several authors have defined as more specific institutions based on non-<a href="Hierarchy">hierarchical</a> <a href="Free association (communism and anarchism)">free associations</a>..<a href="Anarchism">Anarchism</a>'
    test_line_2 = 'CSF pressure, as measured by <a href="lumbar puncture">lumbar puncture</a> (LP), is 10-18 <a href="Pressure#H2O">'
    test_line_3 = 'Anarchism'
    list_hype, text, list_ent_errors,parsing_errors,disambiguation_ent_errors,diez_ent_errors= extract_text_and_hyp(test_line_1, False)
    print(list_hype)
    print(text)
    print()