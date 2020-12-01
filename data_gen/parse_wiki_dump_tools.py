# Utility functions to extract the text and hyperlinks from each page in the Wikipedia corpus.
# 提取文本和超链接
from entities.ent_name_id import *


def extract_text_and_hyp(line, mark_mentions):
    list_hyp = []  # (mention,entities)
    text = ''
    list_ent_errors = 0
    parsing_errors = 0
    disambiguation_ent_errors = 0
    diez_ent_errors = 0

    end_end_hyp = 0
    begin_end_hyp = 0
    begin_start_hyp = line.find('<a href="')
    end_start_hyp = begin_start_hyp + len('<a href="')
    num_mentions = 0

    while begin_start_hyp + 1:
        text = text + line[end_end_hyp:begin_start_hyp]
        next_quotes = line.find('">', end_start_hyp)
        end_quotes = next_quotes + len('">') - 1
        if next_quotes + 1:
            ent_name = line[end_start_hyp:next_quotes]
            begin_end_hyp = line.find('</a>', end_quotes)
            end_end_hyp = begin_end_hyp + len('</a>')
            if begin_end_hyp + 1:
                mention = line[end_quotes + 1:begin_end_hyp]
                mention_maker = False
                good_mention = True
                good_mention = good_mention and (not mention.find('Wikipedia') + 1)
                good_mention = good_mention and (not mention.find('wikipedia') + 1)
                good_mention = good_mention and (len(mention) >= 1)

                if good_mention:
                    i = ent_name.find('wikt:') + 1
                    if i == 1:
                        ent_name = ent_name[5:]
                    ent_name = preprocess_ent_name(ent_name)

                    i = ent_name.find('List of ') + 1
                    if (not i) or (i != 1):
                        if ent_name.find('#') + 1:
                            diez_ent_errors = diez_ent_errors + 1
                        else:
                            ent_wikiId = get_ent_wikiid_from_name(ent_name, True)
                            if ent_wikiId == unk_ent_wikiid:
                                disambiguation_ent_errors = disambiguation_ent_errors + 1
                            else:
                                # A valid (entity,mention) pair
                                num_mentions = num_mentions + 1
                                hyp = {'mention': mention, 'ent_wikiid': ent_wikiId, 'cnt': num_mentions}
                                list_hyp.append(hyp)
                                if mark_mentions:
                                    mention_maker = True
                    else:
                        list_ent_errors = list_ent_errors + 1
                if not mention_maker:
                    if text == '':
                        text = mention
                    else:
                        text = text + ' ' + mention + ' '
                else:
                    text = text + 'MMSTART ' + str(num_mentions) + ' ' + str(mention) + ' MMEND ' + str(
                        num_mentions) + ' '
            else:
                parsing_errors = parsing_errors + 1
                end_end_hyp = 0
                begin_start_hyp = -1
        else:
            parsing_errors = parsing_errors + 1
            begin_start_hyp = -1
        if begin_start_hyp + 1:
            begin_start_hyp = line.find('<a href="', end_start_hyp)
            end_start_hyp = begin_start_hyp + len('<a href="')

    if end_end_hyp:
        text = text + line[end_end_hyp:]
    else:
        if not mark_mentions:
            text = line # Parsing did not succed, but we don't throw this line away.
        else:
            text = ''
            list_hyp = {}

    return list_hyp, text, list_ent_errors, parsing_errors, disambiguation_ent_errors, diez_ent_errors


# Unit tests
if __name__ == '__main__':
    print('\n Unit tests:')
    test_line_1 = '<a href="Anarchism">Anarchism</a> is a <a href="political philosophy">political philosophy</a> that advocates<a href="stateless society">stateless societies</a>often defined as <a href="self-governance">self-governed</a> voluntary institutions, but that several authors have defined as more specific institutions based on non-<a href="Hierarchy">hierarchical</a> <a href="Free association (communism and anarchism)">free associations</a>..<a href="Anarchism">Anarchism</a>'
    test_line_2 = 'CSF pressure, as measured by <a href="lumbar puncture">lumbar puncture</a> (LP), is 10-18 <a href="Pressure#H2O">'
    test_line_3 = 'Anarchism'
    list_hype, text, list_ent_errors,parsing_errors,disambiguation_ent_errors,diez_ent_errors= extract_text_and_hyp(test_line_1, False)
    print(list_hype)
    print(text)

    # list_hype, text, list_ent_errors, parsing_errors, disambiguation_ent_errors, diez_ent_errors= extract_text_and_hyp(test_line_1, True)
    # print(list_hype)
    # print(text)
    # print()

    # list_hype, text, list_ent_errors,parsing_errors,disambiguation_ent_errors,diez_ent_errors= extract_text_and_hyp(test_line_2, True)
    # print(list_hype)
    # print(text)
    # print()

    # list_hype, text, list_ent_errors, parsing_errors, disambiguation_ent_errors, diez_ent_errors = extract_text_and_hyp(
    #     test_line_3, False)
    # print(list_hype)
    # print(text)
    # print()
    # print('    Done unit tests.')
