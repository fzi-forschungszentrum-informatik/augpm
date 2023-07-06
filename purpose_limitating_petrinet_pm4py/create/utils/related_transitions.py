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
from typing import Tuple

from pm4py.objects.petri_net.obj import PetriNet
from pm4py import get_start_activities, get_end_activities


def get_related_transitions(
        log: pd.DataFrame(), net: PetriNet) -> Tuple[dict, dict]:
    '''
    * Create two dictionaries, each containing place.name as keys
    * The first dictionary contains a list of all transitions that are placed
      before the corresponding place
    * The second dictionary contains a list of all transitions that are placed
      after the corresponding place
    '''

    trans_before_map = {}
    trans_after_map = {}

    for place in net.places:

        trans_before = []
        trans_after = []

        if place.name == 'start':
            for key in get_start_activities(log).keys():
                trans_after.append(key)
        elif place.name == 'end':
            for key in get_end_activities(log).keys():
                trans_before.append(key)
        else:
            act_beforeandafter = place.name.split('}, {')
            for transition in net.transitions:
                if transition.name in act_beforeandafter[0]:
                    trans_before.append(transition.name)
                if transition.name in act_beforeandafter[1]:
                    trans_after.append(transition.name)

        trans_before_map.update({place.name: trans_before})
        trans_after_map.update({place.name: trans_after})

    return trans_before_map, trans_after_map
