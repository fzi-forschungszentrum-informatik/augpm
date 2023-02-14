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

from view.utils.decorations import get_earnmarking_decorations
from view.utils.digraph_creator import create_graphviz_digraph


def view_purpose_limitating_petrinet(
        pl_net: PetriNet, pl_im: Marking = None,
        pl_fm: Marking = None, decorations: dict = None):
    '''
    View Purpose Limitating Petrinet

    Parameters
    -----------
    pl_net
        Purpose Limitating Petri Net containing extended places and arcs
    pl_im
        Initial Marking
    pl_fm
        Final Marking
    '''

    pl_decorations = get_earnmarking_decorations(pl_net, decorations)
    pl_digraph = create_graphviz_digraph(
        pl_net, pl_im, pl_fm, decorations=pl_decorations)
    gview.view(pl_digraph)
