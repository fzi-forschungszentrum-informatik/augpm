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


def get_arc_decorations(icpl_net: PetriNet, decorations: dict = None) -> dict:
    '''
    Get arc decorations specifically defined Information Confidentiality 
    and Purpose Limitating Petri Net 
    '''
    if decorations is None:
        decorations = {}

    for arc in icpl_net.arcs:

        if len(arc.purposes) != 0:

            if arc.is_consumption_arc:
                purpose_index = 'G'
            else:
                purpose_index = 'LA'
            a_label = '{} = ['.format(purpose_index)

            for purpose in arc.purposes:
                a_label = a_label + purpose + ', '
            a_label = a_label[:-2] + ']'

            arc_decorations = {'label': a_label,
                                  'penwidth': '1.0', 'labelfontsize': '10'}
            decorations.update({arc: arc_decorations})

    return decorations
