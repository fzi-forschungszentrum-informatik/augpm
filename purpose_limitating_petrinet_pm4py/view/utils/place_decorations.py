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

from pm4py.objects.petri_net.obj import PetriNet


def get_place_decorations(
        icpl_net: PetriNet, decorations: dict = None) -> dict:
    '''
    Get place decorations specifically defined Information Confidentiality
    and Purpose Limitating Petri Net
    '''
    if decorations is None:
        decorations = {}

    for place in icpl_net.places:

        if place.info_object_type is not None:
            if place.info_object_type.personalinformation:
                p_color = 'darkred'
            else:
                p_color = 'darkgreen'
            place_decorations = {
                'xlabel': str(place.info_object_type.name),
                'fontcolor': p_color, 'color': 'black'
            }
            decorations.update({place: place_decorations})

    return decorations
