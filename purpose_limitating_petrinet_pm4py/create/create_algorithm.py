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

import time
from typing import Tuple, Union
import pandas as pd

from pm4py.objects.log.obj import EventLog
from pm4py.objects.petri_net.obj import Marking, PetriNet

from create.utils.consumed_infoobjecttypes import consumed_iot_per_activity
from create.utils.create_basic_petrinet import create_basic_petrinet
from create.utils.produced_infoobjecttypes import produced_iot_per_activity
from create.utils.related_transitions import get_related_transitions
from create.utils.related_places import get_related_places
from create.utils.conducting_resources import get_resources_per_transition
from objects.arc_with_purposes import ArcWithPurposes
from objects.place_iot import PlaceIot
from objects.transition_resources import TransitionResource

from constants import (
    PARAMETER_CONSTANT_ACTIVITY_KEY as ACTIVITY_KEY,
    PARAMETER_CONSTANT_INFO_OBJECT_TYPE as INFO_OBJECT_TYPE,
    PARAMETER_CONSTANT_PERMISSION_PURPOSE as PERMISSION_PURPOSE,
    PARAMETER_CONSTANT_CONSUMPTION_PURPOSE as CONSUMPTION_PURPOSE)


def create_icpl_petrinet(
        log: Union[EventLog, pd.DataFrame], iot_consumed: pd.DataFrame(),
        iot_produced: pd.DataFrame()) -> Tuple[PetriNet, Marking, Marking]:
    '''
    Create Information Confidentiality and Purpose Limitating Petri Net

    Parameters
    ----------
    log
        Event Log storing case_id's, activities, timestamps, resources and 
        their trustworthiness
    iot_consumed
        Pandas Dataframe storing activities, their consumed information object 
        types and their consumption purposes (minimum requirement)
    iot_produced
        Pandas Dataframe storing activities, their produced information object 
        types and if they store personal information (minimum requirement)

    Returns
    ----------
    icpl_net
        Purpose Limitating Petri Net containing extended places and arcs
    icpl_im
        Initial marking
    icpl_fm
        Final marking
    '''

    # create basic Petri Net using PM4Py
    net = create_basic_petrinet(log)

    # create Information Confidentiality and Purpose Limitating Petri Net,
    # transfer properties of input Petri Net
    icpl_net = PetriNet('purpose_limitating_net' + str(time.time()),
                        properties=net.properties)

    # add extended places
    trans_before, trans_after = get_related_transitions(log, net)

    for place in net.places:
        icpl_place = PlaceIot(place, trans_before[place.name],
                              trans_after[place.name])
        icpl_net.places.add(icpl_place)

        if place.name == 'start':
            icpl_im = Marking()
            icpl_im[icpl_place] = 1
        if place.name == 'end':
            icpl_fm = Marking()
            icpl_fm[icpl_place] = 1

    produced_iot, iot_references = produced_iot_per_activity(iot_produced)
    consumed_iot = consumed_iot_per_activity(iot_consumed, iot_references)

    for place in icpl_net.places:

        for transition in trans_before[place.name]:
            if (transition in produced_iot.keys()
                    and (place.name == 'end' or len(produced_iot[transition]) == 1)):
                place.info_object_type = produced_iot[transition][0]
                break

        if place.info_object_type is None:
            consumed_iot_list = []
            for transition in trans_after[place.name]:
                if transition in consumed_iot.keys():
                    consumed_iot_list = (consumed_iot_list
                                         + consumed_iot[transition])

            consumed_iot_set = set(consumed_iot_list)

            # not every place must be assigned to an infoobjecttype
            if len(consumed_iot_set) == 1:
                place.info_object_type = consumed_iot_set.pop()

        if place.info_object_type != None:
            place.confidentiality = place.info_object_type.confidentiality

    # add extended transitions / open question: do we need iot_produced?iot_consumed?
    places_before, places_after = get_related_places(net)
    resources_per_transition = get_resources_per_transition(log)

    for transition in net.transitions:
        pl_transition = TransitionResource(transition, places_before[transition.name],
                                           places_after[transition.name],
                                           resources_per_transition[transition.name])
        icpl_net.transitions.add(pl_transition)

    for transition in icpl_net.transitions:
        for resource in transition.resource:
            if resource.trustworthiness > int(transition.trustworthiness):
                transition.trustworthiness = resource.trustworthiness

    # add extended arcs
    for arc in net.arcs:
        if type(arc.source) == PetriNet.Place:
            corresponding_icpl_source = list(filter(lambda place:
                                                    arc.source.name == place.name,
                                                    icpl_net.places))[0]
            corresponding_icpl_target = list(filter(lambda transition:
                                                    arc.target.name == transition.name,
                                                    icpl_net.transitions))[0]
            icpl_arc = ArcWithPurposes(PetriNet.Arc(corresponding_icpl_source,
                                                    corresponding_icpl_target))
            icpl_net.arcs.add(icpl_arc)
        elif type(arc.target) == PetriNet.Place:
            corresponding_icpl_source = list(filter(lambda transition:
                                                    arc.source.name == transition.name,
                                                    icpl_net.transitions))[0]
            corresponding_icpl_target = list(filter(lambda place:
                                                    arc.target.name == place.name,
                                                    icpl_net.places))[0]
            icpl_arc = ArcWithPurposes(PetriNet.Arc(corresponding_icpl_source,
                                                    corresponding_icpl_target))
            icpl_net.arcs.add(icpl_arc)

    for i in range(0, len(iot_produced)):

        if type(iot_produced.iloc[i].loc[PERMISSION_PURPOSE]) != float:
            corresponding_icpl_arc = list(filter(lambda arc:
                                                 (arc.source.name ==
                                                  iot_produced.iloc[i].loc[ACTIVITY_KEY])
                                                 and (arc.target.info_object_type is not None)
                                                 and (arc.target.info_object_type.name
                                                      == iot_produced.iloc[i].loc[INFO_OBJECT_TYPE]),
                                                 icpl_net.arcs))[0]
            corresponding_icpl_arc.purposes.add(
                str(iot_produced.iloc[i].loc[PERMISSION_PURPOSE]))

    for i in range(0, len(iot_consumed)):
        if type(iot_consumed.iloc[i].loc[CONSUMPTION_PURPOSE]) != float:
            corresponding_icpl_arc = list(filter(lambda arc:
                                                 type(arc.source) == PlaceIot
                                                 and arc.target.name == iot_consumed.iloc[i].loc[ACTIVITY_KEY]
                                                 and arc.source.info_object_type is not None
                                                 and (arc.source.info_object_type.name
                                                      == iot_consumed.iloc[i].loc[INFO_OBJECT_TYPE]),
                                                 icpl_net.arcs))
            if len(corresponding_icpl_arc) == 1:
                corresponding_icpl_arc[0].purposes.add(
                    str(iot_consumed.iloc[i].loc[CONSUMPTION_PURPOSE]))

    # implicit transfer of the permitted purposes by consumption purposes
    for place in icpl_net.places:
        if len(place.trans_before) == 1:
            permission_purposes = set()
            for arc in list(filter(lambda arc:
                                   (arc.source.name
                                       == place.name), icpl_net.arcs)):
                permission_purposes.update(icpl_arc.purposes)
            list(filter(lambda arc:
                        arc.target.name == place.name,
                        icpl_net.arcs))[0].purposes.union(permission_purposes)

    return icpl_net, icpl_im, icpl_fm
