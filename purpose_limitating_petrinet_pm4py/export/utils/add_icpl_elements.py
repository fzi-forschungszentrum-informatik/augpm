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


def add_icpl_elements(icpl_net: PetriNet, tree: ElementTree) -> ElementTree:
    '''
    Add new information of Information Confidentiality and 
    Purpose Limitating Petri Net in form of
    * elements,
    * attributes and
    * text nodes
    to PNML document exported with pm4Py
    '''

    # places
    for place in tree.iter('place'):
        corresponding_icpl_place = list(filter(lambda icpl_place: place.get(
            'id') == icpl_place.name
            and icpl_place.info_object_type is not None,
            icpl_net.places))

        if len(corresponding_icpl_place) == 1:
            informationobjecttype = etree.SubElement(
                place, "informationobjecttype",
                id=corresponding_icpl_place[0].info_object_type.name,
                personalinformation=str(
                    corresponding_icpl_place[0].info_object_type.personalinformation),
                confidentiality=str(corresponding_icpl_place[0].confidentiality))  # neu
            informationobjecttype_text = etree.SubElement(
                informationobjecttype, "text")
            informationobjecttype_text.text = corresponding_icpl_place[0].info_object_type.name

  # transitions
    for transition in tree.iter('transition'):
        corresponding_icpl_transition = list(filter(lambda icpl_transition: transition.get(
            'id') == icpl_transition.name
            and icpl_transition.resource is not None,
            icpl_net.transitions))

        if len(corresponding_icpl_transition) == 1:
            for i in corresponding_icpl_transition[0].resource:
                res = etree.SubElement(
                    transition, "resource",
                    id=i.name,
                    trustworthiness=str(
                        i.trustworthiness))
                res_text = etree.SubElement(
                    res, "text")
                res_text.text = i.name

    # arcs
    for arc in tree.iter('arc'):
        corresponding_icpl_arc = list(filter(lambda pl_arc: arc.get('id') == str(
            hash(pl_arc)) and len(pl_arc.purposes) > 0, icpl_net.arcs))

        if len(corresponding_icpl_arc) == 1:
            arc.set("consumption", str(
                corresponding_icpl_arc[0].is_consumption_arc))
            purposes = etree.SubElement(arc, "purposes")
            purposes_text = etree.SubElement(purposes, "text")
            purposes_text.text = str(corresponding_icpl_arc[0].purposes)

    return tree
