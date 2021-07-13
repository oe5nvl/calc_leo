################################################################
# Deep Space Set_Oberating_Mode
# Groundstation software
# (c) oe5nvl, oe5rnl
#

import calc_obj
leos = calc_obj.Leos(__import__('config_dss_c'))

all_obj_data = leos.calc_all()

print(all_obj_data)