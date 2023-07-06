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
from typing import Tuple

from objects.place_iot import InfoObjectType

from constants import (
    PARAMETER_CONSTANT_ACTIVITY_KEY as ACTIVITY_KEY,
    PARAMETER_CONSTANT_INFO_OBJECT_TYPE as INFO_OBJECT_TYPE,
    PARAMETER_CONSTANT_PERSONAL_INFORMATION as PERSONAL_INFORMATION, 
    PARAMETER_CONSTANT_CONFIDENTIALITY as CONFIDENTIALITY)


def produced_iot_per_activity(
        iot_produced: pd.DataFrame()) -> Tuple[dict, dict]:
    '''
    Create dictionary containing activities as keys and list of produced
    information object types as values
    '''

    unique_activities = pd.unique(iot_produced[ACTIVITY_KEY])
    produced_iot = {}

    unique_iot = pd.unique(iot_produced[INFO_OBJECT_TYPE])
    iot_references = {}

    for iot_element in unique_iot:
        iot_references.update({iot_element:""})

    for i in range(0, len(unique_activities)):

        list_help = []
        iot_per_activity = pd.unique(
            iot_produced.loc[(iot_produced[ACTIVITY_KEY]
                              == unique_activities[i])]
            [INFO_OBJECT_TYPE])

        for value in iot_per_activity:

            # if iot not initialized yet, initialize it 
            if type(iot_references[value] == str):

                infoObjectType = InfoObjectType(str(value))

                # personal information
                bool_values = pd.DataFrame(
                    iot_produced.loc[iot_produced[ACTIVITY_KEY]
                                     == unique_activities[i]]
                    [PERSONAL_INFORMATION])
                for j in range(0, len(bool_values)):
                    if (bool_values.iloc[j].loc[PERSONAL_INFORMATION]
                            == 'True'):
                        infoObjectType.personalinformation = True
                        break
                
                # confidentiality
                iot_confidentiality = pd.DataFrame.max(
                    iot_produced.loc[iot_produced[INFO_OBJECT_TYPE]==value]
                    [CONFIDENTIALITY])
                infoObjectType.confidentiality = int(iot_confidentiality)

                iot_references[value] = infoObjectType

            list_help.append(iot_references[value])

        produced_iot.update({unique_activities[i]: list_help})

    return produced_iot, iot_references
