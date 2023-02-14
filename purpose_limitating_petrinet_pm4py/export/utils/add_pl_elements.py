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

from lxml import etree
from lxml.etree import ElementTree
from pm4py.objects.petri_net.obj import PetriNet


def add_pl_elements(pl_net: PetriNet, tree: ElementTree) -> ElementTree:
    '''
    adds new information of Purpose Limitating Petri Net in form of
    * elements,
    * attributes and
    * text nodes
    to PNML document exported with pm4Py
    '''

    # places
    for place in tree.iter('place'):
        corresponding_pl_place = list(filter(lambda pl_place: place.get(
            'id') == pl_place.name
            and pl_place.info_object_type is not None,
            pl_net.places))

        if len(corresponding_pl_place) == 1:
            informationobjecttype = etree.SubElement(
                place, "informationobjecttype",
                id=corresponding_pl_place[0].info_object_type.name,
                personalinformation=str(
                    corresponding_pl_place[0].info_object_type.personalinformation))
            informationobjecttype_text = etree.SubElement(
                informationobjecttype, "text")
            informationobjecttype_text.text = corresponding_pl_place[0].info_object_type.name

    # arcs
    for arc in tree.iter('arc'):
        corresponding_pl_arc = list(filter(lambda pl_arc: arc.get('id') == str(
            hash(pl_arc)) and len(pl_arc.purposes) > 0, pl_net.arcs))

        if len(corresponding_pl_arc) == 1:
            arc.set("consumption", str(
                corresponding_pl_arc[0].is_consumption_arc))
            purposes = etree.SubElement(arc, "purposes")
            purposes_text = etree.SubElement(purposes, "text")
            purposes_text.text = str(corresponding_pl_arc[0].purposes)

    return tree
