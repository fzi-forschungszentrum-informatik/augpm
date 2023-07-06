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


class Resource(object):

    def __init__(self, name, trustworthiness=0):
        '''
        initialize resource by assigning 
        * a name and
        * its trustworthiness
        '''
        self.__name: str() = name
        self.__trustworthiness: int = trustworthiness

    def __get_name(self):
        return self.__name

    def __set_name(self, name):
        self.__name = name

    def __get_trustworthiness(self):
        return self.__trustworthiness

    def __set_trustworthiness(self, trustworthiness):
        self.__trustworthiness = trustworthiness

    name = property(__get_name, __set_name)
    trustworthiness = property(__get_trustworthiness, __set_trustworthiness)


class TransitionResource(PetriNet.Transition):

    def __init__(self, transition, places_before=None,
                 places_after=None, resource=None, trustworthiness=0,
                 iot_produced=None, iot_consumed=None):
        '''
        initialize transition object of Information Confidentiality 
        Petri Net by assigning
        * basic transition attributes of underlying Petri Net,
        * a list of places executed directly before transition,
        * a list of places executed directly after transition, 
        * a set of resources and 
        * its overall trustworthiness

        '''
        super().__init__(
            transition.name, transition.label, transition.in_arcs,
            transition.out_arcs, transition.properties)
        self.__places_before: list[str] = list(
        ) if places_before is None else places_before
        self.__places_after: list[str] = list(
        ) if places_after is None else places_after
        self.__resource: set(Resource) = set(
        ) if resource is None else resource
        self.__trustworthiness = None if trustworthiness is None else trustworthiness

    def __get_places_before(self):
        return self.__places_before

    def __set_places_before(self, places_before):
        self.__places_before = places_before

    def __get_places_after(self):
        return self.__places_after

    def __set_places_after(self, places_after):
        self.__places_after = places_after

    def __get_resource(self):
        return self.__resource

    def __set_resource(self, resource):
        self.__resource = resource

    def __get_trustworthiness(self):
        return self.__trustworthiness

    def __set_trustworthiness(self, trustworthiness):
        self.__trustworthiness = trustworthiness

    places_before = property(__get_places_before, __set_places_before)
    places_after = property(__get_places_after, __set_places_after)
    resource = property(__get_resource, __set_resource)
    trustworthiness = property(__get_trustworthiness, __set_trustworthiness)
