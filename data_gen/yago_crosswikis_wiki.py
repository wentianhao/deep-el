# loads the merged p(e|m) index

import torch
import Utils.utils
import entities.ent_name_id

ent_p_e_m_index = {}

mention_lower_to_one_upper = {}

mention_total_freq = {}

crosswikis_textfilename = ''