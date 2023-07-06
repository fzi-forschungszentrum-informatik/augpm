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

from create.create_algorithm import create_icpl_petrinet
from view.view_algorithm import view_icpl_petrinet
from export.export_algorithm import export_icpl_petrinet


if __name__ == "__main__":

    # required attributes: case_id, activity, timestamp, resource
    # desired attribute: trustworthiness
    log = read_csv(
        'C:/Workspace/AugPM/data/cases_numered_act.csv',
        sep=";", encoding='latin1', dtype='str')

    # required attributes: activity, info_object_type, consumption_purpose
    # desired attributes: case_id, place_from_type
    IT_consumed = read_csv(
        'C:/Workspace/AugPM/data/IT_consumed_act.csv',
        sep=";", encoding='latin1', dtype='str')

    # required attributes: activity, info_object_type, (personal_information),
    # desired attributes: case_id, permitted_purposes
    IT_produced = read_csv(
        'C:/Workspace/AugPM/data/IT_produced_act.csv',
        sep=";", encoding='latin1', dtype='str')

    icpl_net, icpl_im, icpl_fm = create_icpl_petrinet(
        log, IT_consumed, IT_produced)
    view_icpl_petrinet(icpl_net, icpl_im, icpl_fm)
    export_icpl_petrinet(
        icpl_net, icpl_im, icpl_fm,
        'C:/Workspace/AugPM/data/output_pnml.pnml')
