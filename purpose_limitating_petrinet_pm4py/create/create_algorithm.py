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

from create.utils.delete_whitespaces import delete_whitespaces
from create.utils.consumed_infoobjecttypes import consumed_iot_per_activity
from create.utils.create_basic_petrinet import create_basic_petrinet
from create.utils.produced_infoobjecttypes import produced_iot_per_activity
from create.utils.related_transitions import get_related_transitions
from objects.arc_with_purposes import ArcWithPurposes
from objects.place_iot import PlaceIot

from constants import (
    PARAMETER_CONSTANT_ACTIVITY_KEY as ACTIVITY_KEY,
    PARAMETER_CONSTANT_INFO_OBJECT_TYPE as INFO_OBJECT_TYPE,
    PARAMETER_CONSTANT_PERMISSION_PURPOSE as PERMISSION_PURPOSE,
    PARAMETER_CONSTANT_CONSUMPTION_PURPOSE as CONSUMPTION_PURPOSE)


def create_purpose_limitating_petrinet(
        log: Union[EventLog, pd.DataFrame], iot_consumed: pd.DataFrame(),
        iot_produced: pd.DataFrame()) -> Tuple[PetriNet, Marking, Marking]:
    '''
    Create Purpose Limitating Petri Net

    Parameters
    ----------
    log
        Event Log storing case_id's, activities and timestamps
    iot_consumed
        Pandas Dataframe storing activities, their consumed information object 
        types and their consumption purposes (minimum requirement)
    iot_produced
        Pandas Dataframe storing activities, their produced information object 
        types and if they store personal information (minimum requirement)

    Returns
    ----------
    pl_net
        Purpose Limitating Petri Net containing extended places and arcs
    pl_im
        Initial marking
    pl_fm
        Final marking
    '''

    # delete whitespaces to ensure correct assignments
    #log, iot_produced, iot_consumed = delete_whitespaces(
    #    log, iot_produced, iot_consumed)

    # create basic Petri Net using PM4Py
    net = create_basic_petrinet(log)

    # create Purpose Limitating Petri Net and transfer transitions and
    # properties of input Petri Net
    pl_net = PetriNet('purpose_limitating_net' + str(time.time()),
                      transitions=net.transitions, properties=net.properties)

    # add extended places
    trans_before, trans_after = get_related_transitions(log, net)

    for place in net.places:
        pl_place = PlaceIot(place, trans_before[place.name],
                            trans_after[place.name])
        pl_net.places.add(pl_place)

        if place.name == 'start':
            pl_im = Marking()
            pl_im[pl_place] = 1
        if place.name == 'end':
            pl_fm = Marking()
            pl_fm[pl_place] = 1

    produced_iot, iot_references = produced_iot_per_activity(iot_produced)
    consumed_iot = consumed_iot_per_activity(iot_consumed, iot_references)

    for pl_place in pl_net.places:

        for transition in trans_before[pl_place.name]:
            if (transition in produced_iot.keys()
                    and (pl_place.name == 'end' or len(produced_iot[transition]) == 1)):
                pl_place.info_object_type = produced_iot[transition][0]
                break

        if pl_place.info_object_type is None:
            consumed_iot_list = []
            for transition in trans_after[pl_place.name]:
                if transition in consumed_iot.keys():
                    consumed_iot_list = (consumed_iot_list
                                         + consumed_iot[transition])

            consumed_iot_set = set(consumed_iot_list)

            # not every place must be assigned to an infoobjecttype
            if len(consumed_iot_set) == 1:
                pl_place.info_object_type = consumed_iot_set.pop()

    # add extended arcs
    for arc in net.arcs:
        if type(arc.source) == PetriNet.Place:
            corresponding_pl_source = list(filter(lambda pl_place:
                                           arc.source.name == pl_place.name,
                                           pl_net.places))[0]
            pl_arc = ArcWithPurposes(PetriNet.Arc(corresponding_pl_source,
                                                  arc.target))
            pl_net.arcs.add(pl_arc)
        elif type(arc.target) == PetriNet.Place:
            corresponding_pl_target = list(filter(lambda em_place:
                                           arc.target.name == em_place.name,
                                           pl_net.places))[0]
            em_arc = ArcWithPurposes(PetriNet.Arc(arc.source,
                                                  corresponding_pl_target))
            pl_net.arcs.add(em_arc)

    for i in range(0, len(iot_produced)):

        if type(iot_produced.iloc[i].loc[PERMISSION_PURPOSE]) != float:
            corresponding_ppl_arc = list(filter(lambda pl_arc:
                                                (pl_arc.source.name ==
                                                 iot_produced.iloc[i].loc[ACTIVITY_KEY])
                                                and (pl_arc.target.info_object_type is not None)
                                                and (pl_arc.target.info_object_type.name
                                                     == iot_produced.iloc[i].loc[INFO_OBJECT_TYPE]),
                                                pl_net.arcs))[0]
            corresponding_ppl_arc.purposes.add(
                str(iot_produced.iloc[i].loc[PERMISSION_PURPOSE]))

    for i in range(0, len(iot_consumed)):
        if type(iot_consumed.iloc[i].loc[CONSUMPTION_PURPOSE]) != float:
            corresponding_cpl_arc = list(filter(lambda pl_arc:
                                                type(pl_arc.source) == PlaceIot
                                                and pl_arc.target.name == iot_consumed.iloc[i].loc[ACTIVITY_KEY]
                                                and pl_arc.source.info_object_type is not None
                                                and (pl_arc.source.info_object_type.name
                                                     == iot_consumed.iloc[i].loc[INFO_OBJECT_TYPE]),
                                                pl_net.arcs))
            if len(corresponding_cpl_arc) == 1: 
                corresponding_cpl_arc[0].purposes.add(
                    str(iot_consumed.iloc[i].loc[CONSUMPTION_PURPOSE]))

    # implicit transfer of the permitted purposes by consumption purposes
    for pl_place in pl_net.places:
        if len(pl_place.trans_before) == 1:
            permission_purposes = set()
            for pl_arc in list(filter(lambda pl_arc:
                                      (pl_arc.source.name
                                       == pl_place.name), pl_net.arcs)):
                permission_purposes.update(pl_arc.purposes)
            list(filter(lambda pl_arc:
                        pl_arc.target.name == pl_place.name,
                        pl_net.arcs))[0].purposes.union(permission_purposes)

    return pl_net, pl_im, pl_fm
