## augPM
AugPM is a prototype for the generation of augmented process mining results.

The first version of augPM was implemented at the FZI Forschungszentrum Informatik (https://www.fzi.de) by Maria Weinreuter between October 2022 and February 2023.

AugPM was first developed for the example of analysing purpose limitation of personal data in business processes. For this purpose, purpose limitating petri nets were used (as described as part of the ICPN in Alpers 2019, see https://www.doi.org/10.5445/KSP/1000094545). The concepts of augPM can be applied to other business process log analysis problems in the future.

We use PM4Py (https://github.com/pm4py) as a preliminary work for augPM. Our work has strong dependencies on PM4Py. Therefore, a PM4Py environment needs to be installed.


## Acknowledgements
AugPM is partly a result of the "SofDCar Software-Defined Car" (https://sofdcar.de) project with eight industry partners and four research partners. This project was supported by the German Federal Ministry for Economic Affairs and Climate Action (https://www.bmwk.de) by decision of the German Bundestag (https://www.bundestag.de).


## Licence
- Please refer to the LICENSE.txt and the header in the various source files.
- The implementation is released under the GPLv3 licence.
- One reason is that the preliminary work PM4Py uses the same licence (consider licence information in the PM4Py GitHub project).

## How to get started
First of all, to get augPM running, you need to get PM4Py running. Installation guides for all types of operation systems can be found on the PM4Py homepage: https://pm4py.fit.fraunhofer.de/install. 

If all necessary programs for PM4Py are successfully installed, augPM can be used successfully. 
To be able to execute the "DEMO.py" file, the paths to export and import the demonstration data must be changed. 
The paths need to be defined in lines 28, 34, 40 (import .csv files) and 47 (export .pnml file).