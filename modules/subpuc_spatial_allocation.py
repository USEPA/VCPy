import numpy as np

####################################################################################################
### These functions generate TOG/VOC csv files for each sub-PUC by state and county.
####################################################################################################

####################################################################################################
def annual_population(year,tot_population):
    for i in range(len(tot_population[0,2:])):
        if tot_population[0,2+i] == year:
            annual_pop = np.sum(tot_population[1:,2+i])
        else: pass
    return annual_pop
####################################################################################################

####################################################################################################
def allocate(year,subpuc_names,annual_pop):

    ################################################################################################
    ### Import State and County spatial allocation data. 
    state_allocation  = np.genfromtxt('./input/allocation/subpuc_state_allocation_'+str(year)+'.csv',delimiter=',',skip_header=1)  # fipstate, fipcty, count for every sub-PUC
    county_allocation = np.genfromtxt('./input/allocation/subpuc_county_allocation_'+str(year)+'.csv',delimiter=',',skip_header=1) # fipstate, fipcty, count for every sub-PUC
    ### Import sub-PUC TOG emissions.
    subPUC_TOG_emis   = np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(7))    # volatile.emission.kg/person/yr
    ### Import sub-PUC VOC emissions.
    subPUC_VOC_emis   = np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(9))    # VOC.emission.kg/person/yr
    ################################################################################################

    ################################################################################################
    ### Initialize the final arrays. 
    ### Final emissions, State-level [Gg/year]
    final_state_TOG_array         = np.zeros((len(state_allocation),len(subPUC_TOG_emis)+2))
    final_state_TOG_array[:,0:2]  = state_allocation[:,0:2]
    final_state_VOC_array         = np.zeros((len(state_allocation),len(subPUC_VOC_emis)+2))
    final_state_VOC_array[:,0:2]  = state_allocation[:,0:2]
    ### Final emissions, County-level [kg/year]
    final_county_TOG_array        = np.zeros((len(county_allocation),len(subPUC_TOG_emis)+2))
    final_county_TOG_array[:,0:2] = county_allocation[:,0:2]
    final_county_VOC_array        = np.zeros((len(county_allocation),len(subPUC_VOC_emis)+2))
    final_county_VOC_array[:,0:2] = county_allocation[:,0:2]
    ################################################################################################

    ################################################################################################
    ### Calculate State-level and County-level emissions for each unspeciated sub-PUC
    subPUC_TOG_emis              = subPUC_TOG_emis[:] * annual_pop
    subPUC_VOC_emis              = subPUC_VOC_emis[:] * annual_pop

    total_state_allocation       = np.sum(state_allocation[:,2:],axis=0)
    total_county_allocation      = np.sum(county_allocation[:,2:],axis=0)

    state_allocation[:,2:]       = state_allocation[:,2:]  / total_state_allocation[:]
    county_allocation[:,2:]      = county_allocation[:,2:] / total_county_allocation[:]

    final_state_TOG_array[:,2:]  = state_allocation[:,2:]  * subPUC_TOG_emis[:] / 1e6
    final_county_TOG_array[:,2:] = county_allocation[:,2:] * subPUC_TOG_emis[:]
    final_state_VOC_array[:,2:]  = state_allocation[:,2:]  * subPUC_VOC_emis[:] / 1e6
    final_county_VOC_array[:,2:] = county_allocation[:,2:] * subPUC_VOC_emis[:]

    print("Total National VCP Emissions [Tg/year]: ",np.round(np.nansum(subPUC_TOG_emis[:])/1e9,2))
    ################################################################################################

    ################################################################################################
    ### 
    headerline1   = 'fipstate,fipscty,'+np.array2string(subpuc_names[:],max_line_width=1e6,separator=',') 
    headerline2   = 'All emissions reported in Gg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/subpuc_state_TOG_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_state_TOG_array[:],delimiter=',',header=headerline)
    ################################################################################################

    ################################################################################################
    ###
    headerline1   = 'fipstate,fipscty,'+np.array2string(subpuc_names[:],max_line_width=1e6,separator=',') 
    headerline2   = 'All emissions reported in kg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/subpuc_county_TOG_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_county_TOG_array[:],delimiter=',',header=headerline)
    ################################################################################################

    ################################################################################################
    ### 
    headerline1   = 'fipstate,fipscty,'+np.array2string(subpuc_names[:],max_line_width=1e6,separator=',') 
    headerline2   = 'All emissions reported in Gg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/subpuc_state_VOC_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_state_VOC_array[:],delimiter=',',header=headerline)
    ################################################################################################

    ################################################################################################
    ###
    headerline1   = 'fipstate,fipscty,'+np.array2string(subpuc_names[:],max_line_width=1e6,separator=',') 
    headerline2   = 'All emissions reported in kg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/subpuc_county_VOC_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_county_VOC_array[:],delimiter=',',header=headerline)
    ################################################################################################

####################################################################################################