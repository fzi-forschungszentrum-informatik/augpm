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

from export.utils.add_icpl_elements import add_icpl_elements
from export.utils.export_petri_tree import export_petri_tree


def export_icpl_petrinet(
        icpl_net: PetriNet, icpl_im: Marking,
        icpl_fm: Marking, output_filepath: str):
    '''
    Export Information COnfidentiality and Purpose Limitating 
    Petri Net to PNML file

    Parameters
    ----------
    icpl_net
        Information Confidentiality and Purpose Limitating 
        Petri Net containing extended places and arcs
    icpl_im
        Initial marking
    icpl_fm
        Final marking
    output_filepath
        filepath on which PNML file should be stored
    '''
    # via PM4Py
    tree = export_petri_tree(icpl_net, icpl_im, icpl_fm)

    # add elements of Information Confidentiality and
    # Purpose Limitating Petri Net
    tree = add_icpl_elements(icpl_net, tree)

    # write pnml file for Information Confidentiality and
    # Purpose Limitating Petri Net
    tree.write(output_filepath, pretty_print=True,
               xml_declaration=True, encoding='UTF-8')
