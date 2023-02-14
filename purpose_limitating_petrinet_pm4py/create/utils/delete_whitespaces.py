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

from typing import Tuple, Union
import pandas as pd
from pm4py.objects.log.obj import EventLog

from constants import (
    PARAMETER_CONSTANT_ACTIVITY_KEY as ACTIVITY_KEY,
    PARAMETER_CONSTANT_INFO_OBJECT_TYPE as INFO_OBJECT_TYPE,
    PARAMETER_CONSTANT_PERMISSION_PURPOSE as PERMISSION_PURPOSE,
    PARAMETER_CONSTANT_CONSUMPTION_PURPOSE as CONSUMPTION_PURPOSE)


def delete_whitespaces(
        log: Union[EventLog, pd.DataFrame], iot_consumed: pd.DataFrame(),
        iot_produced: pd.DataFrame()):
    '''
    Delete whitespaces in cells containing strings to ensure
    correct string comparisons in further algorithms
    '''

    if type(log) == pd.DataFrame:
        log[ACTIVITY_KEY].str.strip()
    elif type(log) == EventLog:
        for i in range(0, len(log)):
            for j in range(0, len(log[i])):
                log[i][j][ACTIVITY_KEY].strip()

    iot_produced[ACTIVITY_KEY].str.strip()
    iot_produced[INFO_OBJECT_TYPE].str.strip()
    iot_produced[PERMISSION_PURPOSE].str.strip()

    iot_consumed[ACTIVITY_KEY].str.strip()
    iot_consumed[INFO_OBJECT_TYPE].str.strip()
    iot_consumed[CONSUMPTION_PURPOSE].str.strip()

    return log, iot_produced, iot_consumed
