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

from objects.transition_resources import Resource

from constants import (
    PARAMETER_CONSTANT_ACTIVITY_KEY as ACTIVITY_KEY,
    PARAMETER_CONSTANT_RESOURCE as RESOURCE, 
    PARAMETER_CONSTANT_TRUSTWORTHINESS as TRUSTWORTHINESS)

def get_resources_per_transition(
        log: pd.DataFrame()) -> dict:
    '''
    Create dictionary containing activities as keys and list of 
    resources as values
    '''

    unique_activities = pd.unique(log[ACTIVITY_KEY])
    activity_resource_dict = {}

    unique_resources = pd.unique(log[RESOURCE])
    resource_references = {}

    for resource in unique_resources:
        resource_references.update({resource:""})

    for i in range(0, len(unique_activities)):
        list_help = []
        resources_per_activity = pd.unique(
                            log.loc[(log[ACTIVITY_KEY]
                              == unique_activities[i])][RESOURCE])

        for resource in resources_per_activity:
           
            # if ressource not initialized yet, initialize it 
            if type(resource_references[resource]) == str:
                resource_initialized = Resource(str(resource))
                min_ranking = pd.DataFrame.min(
                    log.loc[log[RESOURCE]
                                     == resource]
                                     [TRUSTWORTHINESS])
                resource_initialized.trustworthiness = int(min_ranking)
                resource_references[resource] = resource_initialized

            list_help.append(resource_references[resource])

        activity_resource_dict.update(
            {unique_activities[i]: list_help})

    return activity_resource_dict