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
from pm4py.objects.petri_net.exporter.variants.pnml import export_petri_tree

from export.utils.add_pl_elements import add_pl_elements
from export.utils.export_petri_tree import export_petri_tree


def export_purpose_limitating_petrinet(
        pl_net: PetriNet, pl_im: Marking,
        pl_fm: Marking, output_filepath: str):
    '''
    Export Purpose Limitating Petri Net to PNML file

    Parameters
    ----------
    pl_net
        Purpose Limitating Petri Net containing extended places and arcs
    pl_im
        Initial marking
    pl_fm
        Final marking
    output_filepath
        filepath on which PNML file should be stored
    '''
    # via PM4Py
    tree = export_petri_tree(pl_net, pl_im, pl_fm)

    # add elements of Purpose Limitating Petri Net
    tree = add_pl_elements(pl_net, tree)

    # write pnml file for Purpose Limitating Petri Net
    tree.write(output_filepath, pretty_print=True,
               xml_declaration=True, encoding='UTF-8')
