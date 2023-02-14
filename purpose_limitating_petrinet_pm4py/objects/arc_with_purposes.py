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
from objects.place_iot import PlaceIot


class ArcWithPurposes(PetriNet.Arc):

    def __init__(self, arc, purposes=None):
        '''
        initialize arc object of Purpose Limitating Petri Net by assigning
        * basic arc attributes of underlying Petri Net,
        * a set of purposes and
        * information whether the arc is a consumption or production arc
        '''
        super().__init__(arc.source, arc.target, arc.weight, arc.properties)
        self.__purposes: set[str] = set() if purposes is None else purposes
        self.__is_consumption_arc: bool = True if type(
            arc.source) == PlaceIot else False

    def __set_purposes(self, purposes):
        self.__purposes = purposes

    def __get_purposes(self):
        return self.__purposes

    def __set_is_consumption_arc(self, is_consumption_arc):
        self.__is_consumption_arc = is_consumption_arc

    def __get_is_consumption_arc(self):
        return self.__is_consumption_arc

    purposes = property(__get_purposes, __set_purposes)
    is_consumption_arc = property(
        __get_is_consumption_arc, __set_is_consumption_arc)
