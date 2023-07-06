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

import tempfile

from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.obj import Marking
from graphviz import Digraph


def create_graphviz_digraph(
        icpl_net: PetriNet, icpl_im: Marking = None,
        icpl_fm: Marking = None, decorations: dict = None,
        image_format: str = "png") -> Digraph:
    '''
    Provide visualization for the Purpose Limitating Petri Net

    Parameters
    ----------
    icpl_net
        Information Confidentiality and Purpose Limitating Petri Net 
        containing extended transitions, places and arcs
    icpl_im
        Initial marking
    icpl_fm
        Final marking
    decorations
        Decorations of the Purpose Limitating Petri net 
        (says how element must be presented)
    image_format
        Format that should be associated to the image

    Returns
    -------
    icpl_digraph
        Returns a graphviz Digraph object
    '''

    if icpl_im is None:
        icpl_im = Marking()
    if icpl_fm is None:
        icpl_fm = Marking()
    if decorations is None:
        decorations = {}

    filename = tempfile.NamedTemporaryFile(suffix='.gv')
    icpl_digraph = Digraph(
        icpl_net.name, filename=filename.name, engine='dot',
        graph_attr={'bgcolor': 'white', 'rankdir': 'LR'})

    # transitions
    icpl_digraph.attr('node', shape='box',
                      color='black', style='filled',
                      fillcolor='grey85', fontsize='12')

    for t in icpl_net.transitions:
        if (t in decorations and
                "xlabel" in decorations[t]):
            with icpl_digraph.subgraph(name='cluster'+str(id(t))) as c:
                c.attr(label=decorations[t]['xlabel'], fillcolor='white',
                       fontcolor=decorations[t]['fontcolor'], labelloc='b',
                       peripheries='0')
                c.node(str(id(t)), t.label)
        else:
            icpl_digraph.node(str(id(t)), str(t.label))

    # places
    icpl_digraph.attr('node', shape='circle', fixedsize='true',
                      width='0.75', color='black', style='filled',
                      fillcolor='grey85', fontsize='12')

    # add places, in order by their (unique) name, to avoid undeterminism
    # in the visualization
    places_sort_list_im = sorted(
        [x for x in list(icpl_net.places) if x in icpl_im], key=lambda x: x.name)
    places_sort_list_fm = sorted([x for x in list(icpl_net.places)
                                  if x in icpl_fm and x not in icpl_im],
                                 key=lambda x: x.name)
    places_sort_list_not_im_fm = sorted(
        [x for x in list(icpl_net.places)
         if x not in icpl_im and x not in icpl_fm],
        key=lambda x: x.name)
    places_sort_list = (places_sort_list_im
                        + places_sort_list_not_im_fm + places_sort_list_fm)

    for p in places_sort_list:
        if p.info_object_type is None:
            if p in icpl_im:
                icpl_digraph.node(str(id(p)), '\u25CF',
                                  fontsize='40', fontcolor='black')
            elif p in icpl_fm:
                icpl_digraph.node(str(id(p)), '\u25A0', fontcolor='black',
                                  fontsize='40', peripheries='2')
            else:
                if (
                    p in decorations
                    and 'color' in decorations[p]
                    and 'label' in decorations[p]
                ):
                    icpl_digraph.node(
                        str(id(p)), decorations[p]['label'],
                        color=decorations[p]['color'])
                else:
                    icpl_digraph.node(str(id(p)), "")
        else:
            if p in icpl_im:

                with icpl_digraph.subgraph(name='cluster'+str(id(p))) as c:
                    c.attr(label=decorations[p]['xlabel'], fillcolor='white',
                           fontcolor=decorations[p]['fontcolor'], labelloc='b',
                           peripheries='0')
                    c.node(str(id(p)), '\u25CF', fontsize='40', color='black')

            elif p in icpl_fm:

                with icpl_digraph.subgraph(name='cluster'+str(id(p))) as c:
                    c.attr(label=decorations[p]['xlabel'], fillcolor='white',
                           fontcolor=decorations[p]['fontcolor'], labelloc='b',
                           peripheries='0')
                    c.node(str(id(p)), '\u25A0', fontsize='40', color='black',
                           peripheries='2')

            else:
                if (
                    p in decorations
                    and 'color' in decorations[p]
                    and 'label' in decorations[p]
                ):
                    with icpl_digraph.subgraph(name='cluster'+str(id(p))) as c:
                        c.attr(label=decorations[p]['xlabel'], fillcolor='white',
                               fontcolor=decorations[p]['fontcolor'], labelloc='b',
                               peripheries='0')
                        c.node(
                            str(id(p)), decorations[p]['label'], color=decorations[p]['color'])
                else:
                    with icpl_digraph.subgraph(name='cluster'+str(id(p))) as c:
                        c.attr(label=decorations[p]['xlabel'], fillcolor='white',
                               fontcolor=decorations[p]['fontcolor'], labelloc='b',
                               peripheries='0')
                        c.node(str(id(p)), '')

    # arcs
    arcs_sort_list = sorted(
        list(icpl_net.arcs), key=lambda x: (x.source.name, x.target.name))
    for a in arcs_sort_list:
        if (
            a in decorations
            and 'label' in decorations[a]
            and 'penwidth' in decorations[a]
            and 'labelfontsize' in decorations[a]
        ):
            icpl_digraph.edge(
                str(id(a.source)), str(id(a.target)),
                label=decorations[a]['label'], fontsize='12',
                penwidth=decorations[a]['penwidth'],
                labelfontsize=decorations[a]['labelfontsize'])
        elif a in decorations and 'color' in decorations[a]:
            icpl_digraph.edge(str(id(a.source)), str(id(a.target)),
                              color=decorations[a]['color'], fontsize='12')
        else:
            icpl_digraph.edge(str(id(a.source)), str(
                id(a.target)), fontsize='12')

    icpl_digraph.attr(overlap='false')

    icpl_digraph.format = image_format

    return icpl_digraph
    