'''
    This file is part of augPM.
    
    augPM is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    augPM is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with augPM.  If not, see <https://www.gnu.org/licenses/>.
'''

import pandas as pd
from typing import Union, Tuple

from pm4py.objects.log.obj import EventLog
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py import format_dataframe, discover_petri_net_alpha

from constants import (
    PARAMETER_CONSTANT_CASE_ID as CASE_ID,
    PARAMETER_CONSTANT_ACTIVITY_KEY as ACTIVITY_KEY,
    PARAMETER_CONSTANT_TIMESTAMP_KEY as TIMESTAMP_KEY)


def create_basic_petrinet(
        log: Union[EventLog, pd.DataFrame]) -> Tuple[
            PetriNet, Marking, Marking]:
    '''
    Create basic Petrinet using PM4Py
    '''

    if type(log) == pd.core.frame.DataFrame:
        log = format_dataframe(
            log, case_id=CASE_ID, activity_key=ACTIVITY_KEY,
            timestamp_key=TIMESTAMP_KEY)

    net, im, fm = discover_petri_net_alpha(log)

    return net
