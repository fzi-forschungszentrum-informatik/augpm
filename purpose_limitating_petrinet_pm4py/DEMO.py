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

from pandas import read_csv

from create.create_algorithm import create_purpose_limitating_petrinet
from view.view_algorithm import view_purpose_limitating_petrinet
from export.export_algorithm import export_purpose_limitating_petrinet


if __name__ == "__main__":

    # notw. Attribute: case_id, activity, timestamp
    log = read_csv(
        'C:/Workspace/data/cases_numered_act.csv',
        sep=";", encoding='latin1', dtype='str')

    # notw. Attribute: activity, info_object_type,
    # consumption_purpose, opt. Attribute: case_id, place_from_type
    IT_consumed = read_csv(
        'C:/Workspace/data/IT_consumed_act.csv',
        sep=";", encoding='latin1', dtype='str')

    # notw. Attribute: activity, info_object_type, (personal_information),
    # opt. Attribute: case_id, permitted_purposes
    IT_produced = read_csv(
        'C:/Workspace/data/IT_produced_act.csv',
        sep=";", encoding='latin1', dtype='str')

    pl_net, pl_im, pl_fm = create_purpose_limitating_petrinet(
        log, IT_consumed, IT_produced)
    view_purpose_limitating_petrinet(pl_net, pl_im, pl_fm)
    export_purpose_limitating_petrinet(
        pl_net, pl_im, pl_fm, 'C:/Workspace/purpose_limitating_petri_net/pnml.pnml')
