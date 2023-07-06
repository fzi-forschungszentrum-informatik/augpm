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


class InfoObjectType(object):

    def __init__(self, name, personalinformation=False, confidentiality=0):
        '''
        initialize information object type by assigning 
        * a name, 
        * information whether it contains personal information or not and
        * its confidentiality
        '''
        self.__name: str = name
        self.__personalinformation: bool = personalinformation
        self.__confidentiality: int = confidentiality

    def __get_name(self):
        return self.__name

    def __set_name(self, name):
        self.__name = name

    def __get_personalinformation(self):
        return self.__personalinformation

    def __set_personalinformation(self, personalinformation):
        self.__personalinformation = personalinformation

    def __get_confidentiality(self):
        return self.__confidentiality

    def __set_confidentiality(self, confidentiality):
        self.__confidentiality = confidentiality

    name = property(__get_name, __set_name)
    personalinformation = property(
        __get_personalinformation, __set_personalinformation)
    confidentiality = property(
        __get_confidentiality, __set_confidentiality)


class PlaceIot(PetriNet.Place):

    def __init__(
            self, place, trans_before=None, trans_after=None,
            info_object_type=None, confidentiality=0):
        '''
        initialize place object of Information Confidentiality and 
        Purpose Limitating Petri Net by assigning
        * basic place attributes of underlying Petri Net,
        * a list of transitions executed directly before place,
        * a list of transitions executed directly after place,
        * an information object type that is produced by activities before or may
          be consumed by activities behind the place and 
        * its overall confidentiality 
        '''
        super().__init__(
            place.name, place.in_arcs,
            place.out_arcs, place.properties)
        self.__trans_before: list[str] = list(
        ) if trans_before is None else trans_before
        self.__trans_after: list[str] = list(
        ) if trans_after is None else trans_after
        self.__info_object_type: InfoObjectType = info_object_type
        self.__confidentiality: int = confidentiality

    def __get_trans_before(self):
        return self.__trans_before

    def __set_trans_before(self, trans_before):
        self.__trans_before = trans_before

    def __get_trans_after(self):
        return self.__trans_after

    def __set_trans_after(self, trans_after):
        self.__trans_after = trans_after

    def __set_info_object_type(self, info_object_type):
        self.__info_object_type = info_object_type

    def __get_info_object_type(self):
        return self.__info_object_type

    def __get_confidentiality(self):
        return self.__confidentiality

    def __set_confidentiality(self, confidentiality):
        self.__confidentiality = confidentiality

    trans_before = property(__get_trans_before, __set_trans_before)
    trans_after = property(__get_trans_after, __set_trans_after)
    info_object_type = property(
        __get_info_object_type, __set_info_object_type)
    confidentiality = property(
        __get_confidentiality, __set_confidentiality)

