import sys
from datetime import datetime
import numpy as np

startTime = datetime.now()

####################################################################################################
### VCPy: A framework for estimating emissions from volatile chemical products.
### By excuting this file, all of the modules are run and emissions are estimated
### for each year between the STARTYEAR and ENDYEAR.
####################################################################################################

####################################################################################################
### User Input
### Start and end year for execution:
STARTYEAR = '2018'
ENDYEAR   = '2019'
### Generate summary figures (TRUE or FALSE)?
GEN_FIGS  = 'FALSE'
### Generate SMOKE flat files (TRUE or FALSE)? Note: substantially increases execution time.
GEN_FF10  = 'FALSE'
### Location of modules:
sys.path.append('./modules/')
### Evaporation timescale parameters. See Section 2.1.5 of Seltzer et al. 2021 Atmos Chem Phys for more details.
d      = 0.1   # mm; depth
ve     = 30.   # m/hr; mass transfer coefficient
####################################################################################################

####################################################################################################
### Import all input data.
subpuc_names     = np.genfromtxt("./input/subpuc_1st_order_speciation.csv",delimiter=",",skip_header=1,dtype='str',usecols=(1)) 
subpuc_usage     = np.genfromtxt("./input/subpuc_usage.csv",delimiter=",")
subpuc_usetime   = np.genfromtxt("./input/subpuc_usetimescales.csv",delimiter=",",skip_header=1)
subpuc_controls  = np.genfromtxt("./input/subpuc_controls.csv",delimiter=",",skip_header=1)
first_ord_spec   = np.genfromtxt("./input/subpuc_1st_order_speciation.csv",delimiter=",",skip_header=1,usecols=(2,3,4,5)) 
organic_spec     = np.genfromtxt("./input/subpuc_organic_speciation.csv",delimiter=",")
chem_index       = np.genfromtxt("./input/chemical_assignments_index.csv",delimiter=";",skip_header=1,dtype='str',usecols=(0))
chem_props_vars  = np.genfromtxt("./input/chemical_assignments.csv",delimiter=",",skip_header=1,usecols=(1,4,5,6,9,12,13,14))  # SPECIATE_ID, NumC, NumO, MW, Koa, log(C*), SOA Yield, MIR
chem_props_strs  = np.genfromtxt("./input/chemical_assignments.csv",delimiter=",",skip_header=1,dtype='str',usecols=(0,2,3))   # GROUP, HAPS, nonVOCTOG
subpuc_scc_map   = np.genfromtxt("./input/subpuc_SCC_map.csv",delimiter=",",dtype='str',skip_header=1)                         # SCC	PUC_sub-PUC
county_fips      = np.genfromtxt("./input/county_fips_index.csv",delimiter=",",dtype='str',usecols=(0))                        # Index of FIPS IDs
tot_population   = np.genfromtxt("./input/state_population.csv",delimiter=",")                                                 # population count
####################################################################################################

####################################################################################################
### This module contains several functions that perform QA checks on the input files.
import check_inputs
### This module contain a single function that checks for necessary output directories and creates them, if absent.
import check_directories
### This module contains several functions that collectively calculate the total and speciated emissions for all sub-PUCs.
import subpuc_speciation
### This module contains several functions that generate csv files for each sub-PUC ordered by species emissions.
import subpuc_speciation_ordered
### This module contains two functions that generate TOG/VOC csv files for each sub-PUC by state and county.
import subpuc_spatial_allocation
### This module contains a single function that calculates the SOA and O3 potential for all states and counties.
import subpuc_airquality_potential
### This module contains a single function that calculates the total, county-level VCP emissions speciated and ordered.
import speciated_spatial_allocation
### This module contains several functions that generate summary figures for QA purposes.
import figures
####################################################################################################

years2loop  = np.arange(int(STARTYEAR),int(ENDYEAR)+1,1)

for year in years2loop:
    ### QA check on subpuc_usage.csv file
    check_inputs.check_usage(subpuc_names,year,subpuc_usage)
    ### QA check on subpuc_usetimescales.csv file
    check_inputs.check_usetime(subpuc_names,subpuc_usetime)
    ### QA check on subpuc_controls.csv file
    check_inputs.check_controls(subpuc_names,subpuc_controls)
    ### QA check on subpuc_1st_order_speciation.csv file
    check_inputs.check_1st_order_spec(subpuc_names,first_ord_spec)
    ### QA check on subpuc_organic_speciation.csv file
    check_inputs.check_organic_spec(subpuc_names,organic_spec,chem_index)
    ### QA check on chemical_assignments.csv file
    check_inputs.check_chem_assignments(chem_props_vars,chem_props_strs,chem_index)
    ### QA check on subpuc_SCC_map.csv file
    check_inputs.check_subpuc_SCC_map(subpuc_scc_map,subpuc_names)

    ### Checks for necessary output directories and creates them, if absent.
    check_directories.check_create_directory(year)

    ### Calculate evaporation timescale for all compounds
    evaptime = subpuc_speciation.calc_evaptime(d,ve,chem_props_vars)
    ### Calculate carbon mass of all compounds
    c_mass = subpuc_speciation.calc_c_mass(chem_props_vars)
    ### Extract year-specific usage
    year_specific_usage = subpuc_speciation.year_specific_usage(year,subpuc_usage)
    ### Calculate total and speciated sub-PUC emissions
    subpuc_speciation.calc_subpuc_emis(year,subpuc_names,year_specific_usage,subpuc_usetime,subpuc_controls,first_ord_spec,organic_spec,\
                                       chem_props_vars,chem_props_strs,evaptime,c_mass,subpuc_scc_map)
    
    ### Calculate the O:C ratio for all compounds
    oc_ratio = subpuc_speciation_ordered.oxycar_ratio(chem_props_vars)
    ### Generate organized output for each sub-PUC
    subpuc_speciation_ordered.order_subpucs(year,subpuc_names,chem_index,chem_props_vars,chem_props_strs,oc_ratio)
    ### Generate organized output for total emissions
    subpuc_speciation_ordered.order_total(year,chem_index,chem_props_vars,chem_props_strs,oc_ratio)

    ### Calculates US population for target year
    annual_pop = subpuc_spatial_allocation.annual_population(year,tot_population)
    ### Generate TOG/VOC csv files for each sub-PUC and SCC by state and county
    subpuc_spatial_allocation.allocate(year,subpuc_names,annual_pop)
    ### Generate SMOKE flat file
    if GEN_FF10 == 'TRUE':
        subpuc_spatial_allocation.smoke_flat_file(year)
    elif GEN_FF10 == 'FALSE': pass
    else: print('Check GEN_FF10 entry.')
    
    ### Calculates the SOA and O3 potential for all states and counties.
#    subpuc_airquality_potential.aq_potential(year,subpuc_names)
    
    ### Calculates the total, county-level VCP emissions speciated and ordered for ENDYEAR.
    if int(year) == int(ENDYEAR):
        speciated_spatial_allocation.speciated_allocation(year,chem_index,county_fips)
    else: pass

if GEN_FIGS == 'TRUE':
    ### Generate summary figures
    for loopsubpucs in subpuc_names:
        ### Checks for necessary output directories and creates them, if absent.
        figures.check_create_directory(loopsubpucs)
        ### Generates an array for each year in time series for given sub-PUC.
        subpuc_array = figures.subpuc_timeseries(loopsubpucs,years2loop)
        ### Generates an array for each year in time series for total US population.
        population_array = figures.population_timeseries(years2loop)
        ### Generates a per-capita time series plot.
        figures.percap_timeseries(loopsubpucs,years2loop,subpuc_array)
        ### Generates a total mass time series plot.
        figures.mass_timeseries(loopsubpucs,years2loop,subpuc_array,population_array)
        ### Generates a volatility distribution of sub-PUC emissions for ENDYEAR
        figures.vol_distribution(years2loop,chem_props_vars,chem_props_strs,loopsubpucs,subpuc_names)
    ### Generates an array for each year in time series for total VCP emissions.
    total_array = figures.total_timeseries(years2loop)
    ### Generates an array for each year in time series for total US population.
    population_array = figures.population_timeseries(years2loop)
    ### Generates a per-capita time series plot.
    figures.total_percap_timeseries(years2loop,total_array)
    ### Generates a total mass time series plot.
    figures.total_mass_timeseries(years2loop,total_array,population_array)
    ### Generate a volatility distribution of total emissions for ENDYEAR
    figures.total_vol_distribution(years2loop,chem_props_vars,chem_props_strs)
elif GEN_FIGS == 'FALSE': pass
else: print('Check GEN_FIGS entry.')

print("Time to run VCPy: ",datetime.now() - startTime)