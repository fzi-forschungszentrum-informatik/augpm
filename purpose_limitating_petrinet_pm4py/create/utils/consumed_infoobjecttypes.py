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

import pandas as pd

from objects.place_iot import InfoObjectType

from constants import (
    PARAMETER_CONSTANT_ACTIVITY_KEY as ACTIVITY_KEY,
    PARAMETER_CONSTANT_INFO_OBJECT_TYPE as INFO_OBJECT_TYPE)


def consumed_iot_per_activity(
        iot_consumed: pd.DataFrame(), iot_references: dict = {}) -> dict:
    '''
    Create dictionary containing activities as keys and list of consumed
    information object types as values
    '''

    unique_activities = pd.unique(iot_consumed[ACTIVITY_KEY])
    consumed_iot = {}

    for i in range(0, len(unique_activities)):

        list_help = []
        iot_per_activity = pd.unique(iot_consumed.loc[
            iot_consumed[ACTIVITY_KEY] == unique_activities[i]][
                INFO_OBJECT_TYPE])

        for value in iot_per_activity:

            if (value in iot_references.keys()
                    and type(iot_references[value]) == str):

                infoObjectType = InfoObjectType(str(value))
                iot_references[value] = infoObjectType

            else:
                infoObjectType = InfoObjectType(str(value))
                iot_references.update({value: infoObjectType})

            list_help.append(iot_references[value])

        consumed_iot.update({unique_activities[i]: list_help})

    return consumed_iot
