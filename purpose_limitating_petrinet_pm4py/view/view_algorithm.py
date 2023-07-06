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

from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.visualization.common import gview

from view.utils.decorations import get_icpl_decorations
from view.utils.digraph_creator import create_graphviz_digraph


def view_icpl_petrinet(
        icpl_net: PetriNet, icpl_im: Marking = None,
        icpl_fm: Marking = None, decorations: dict = None):
    '''
    View Information Confidentiality and Purpose Limitating Petrinet

    Parameters
    -----------
    icpl_net
        Information Confidentiality and Purpose Limitating Petri Net 
        containing extended places and arcs
    icpl_im
        Initial Marking
    icpl_fm
        Final Marking
    '''

    icpl_decorations = get_icpl_decorations(icpl_net, decorations)
    icpl_digraph = create_graphviz_digraph(
        icpl_net, icpl_im, icpl_fm, decorations=icpl_decorations)
    gview.view(icpl_digraph)

