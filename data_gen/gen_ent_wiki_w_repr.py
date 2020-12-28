from Utils.utils import *
from data_gen.parse_wiki_dump_tools import *

print('\nExtracting text only from Wiki dump. Output is wiki_canonical_words.txt containing on each line an Wiki entity with the list of all words in its canonical Wiki page.')

out_file = data_dir+'generated/wiki_canonical_words.txt'
ouf = open(out_file,'w')

# find anchors,e.g. <a href="wiki:anarchism">anarchism</a>
num_lines = 0
num_valid_ents = 0
num_error_ents = 0 # Probably list or disambiguation pages
empty_valid_ents = get_map_all_valid_ents()