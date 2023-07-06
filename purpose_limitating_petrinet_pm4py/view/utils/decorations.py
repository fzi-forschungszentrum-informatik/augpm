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

from view.utils.place_decorations import get_place_decorations
from view.utils.transition_decorations import get_transition_decorations
from view.utils.arc_decorations import get_arc_decorations


def get_icpl_decorations(
        icpl_net: PetriNet, decorations: dict = None) -> dict:
    '''
    Get Petri Net decorations to transform it to Information Confidentiality 
    and Purpose Limitating Petri Net

    Parameters
    -------------
    icpl_net
        Petri Net with spezialized PlaceIots, TransitionResources and 
        ArcWithPurposes

    Returns
    -------------
    decorations
        Decorations to use
    '''

    if decorations is None:
        decorations = {}

    # place decorations
    decorations = get_place_decorations(icpl_net, decorations)

    # transition decorations
    decorations = get_transition_decorations(icpl_net, decorations)

    # arc decorations
    decorations = get_arc_decorations(icpl_net, decorations)

    return decorations

    # place decorations
    decorations = get_place_decorations(pl_net, decorations)

    # transition decorations
    decorations = get_transition_decorations(pl_net, decorations)

    # arc decorations
    decorations = get_arc_decorations(pl_net, decorations)

    return decorations
