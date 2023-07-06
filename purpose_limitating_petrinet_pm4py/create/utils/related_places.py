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


def get_related_places(net: PetriNet) -> Tuple[dict, dict]:
    '''
    * Create two dictionaries, each containing transition.name as keys
    * The first dictionary contains a list of all places that are placed
      before the corresponding transiton
    * The second dictionary contains a list of all placed that are placed
      after the corresponding transiton
    '''

    places_before_map = {}
    places_after_map = {}

    for transition in net.transitions:
        places_before = []
        places_after = []

        for arc in net.arcs:
            if transition == arc.source:
                for place in net.places:
                    if place == arc.target:
                        places_after.append(place.name)

            elif transition == arc.target:
                for place in net.places:
                    if place == arc.source:
                        places_before.append(place.name)

        places_before_map.update({transition.name: places_before})
        places_after_map.update({transition.name: places_after})

    return places_before_map, places_after_map