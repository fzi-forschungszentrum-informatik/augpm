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


def get_transition_decorations(
        icpl_net: PetriNet, decorations: dict = None) -> dict:
    '''
    Get transition decorations specifically defined Information Confidentiality 
    and Purpose Limitating Petri Net
    '''
    if decorations is None:
        decorations = {}

    for transition in icpl_net.transitions:

        if transition.resource is not None:
            for resource in transition.resource:

                # set xlabel for transition
                resource_label = (resource.name + " (" +
                                  str(resource.trustworthiness) + ")\n")

                # set color of xlabel for transition
                match resource.trustworthiness:
                    case 0:
                        resource_color = "firebrick2"
                    case 4:
                        resource_color = "chartreuse2"
                    case _:
                        resource_color = "black"

        transition_decorations = {
            'xlabel': resource_label,
            'fontcolor': resource_color}

        decorations.update({transition: transition_decorations})

    return decorations
