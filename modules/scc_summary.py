import sys
import numpy as np
from datetime import datetime

####################################################################################################
### This function generates SCC-specific TOG/VOC summary csv files
####################################################################################################

####################################################################################################
def summary(year,subpuc_names,annual_pop):

    ################################################################################################
    ### Import State and TOG/VOC emissions w/ uncontrols applied. 
    scc_state_TOG            = np.genfromtxt('./output/emissions_spatially_allocated/'+str(year)+'/scc_state_TOG_emissions_'+str(year)+'.csv',delimiter=',',skip_header=2)
    scc_state_VOC            = np.genfromtxt('./output/emissions_spatially_allocated/'+str(year)+'/scc_state_VOC_emissions_'+str(year)+'.csv',delimiter=',',skip_header=2)
    ### Import SCC TOG emissions.
    scc_TOG_emis             = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(9))    # volatile.emission.kg/person/yr
    ### Import SCC VOC emissions.
    scc_VOC_emis             = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(11))   # VOC.emission.kg/person/yr
    ### Import SCC labels.
    scc_labels               = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',dtype='str',delimiter=',',skip_header=1,usecols=(0))    # SCC
    ################################################################################################

    ################################################################################################
    ### Initialize the final arrays. 
    ### Final emissions, SCC-level [short tons/year]
    final_scc_array          = np.zeros((len(scc_labels),10))
    final_scc_array[:,0]     = scc_labels[:]
    ################################################################################################

    ################################################################################################
    ### Calculate emissions for each unspeciated SCC
    final_scc_array[:,1]                = scc_TOG_emis[:] * annual_pop * 0.00110231             # short tons
    final_scc_array[:,2]                = np.sum(scc_state_TOG[:,2:],axis=0) * 1e6 * 0.00110231 # short tons
    final_scc_array[:,3]                = final_scc_array[:,2] - final_scc_array[:,1]           # short tons
    final_scc_array[:,4]                = scc_VOC_emis[:] * annual_pop * 0.00110231             # short tons
    final_scc_array[:,5]                = np.sum(scc_state_VOC[:,2:],axis=0) * 1e6 * 0.00110231 # short tons
    final_scc_array[:,6]                = final_scc_array[:,5] - final_scc_array[:,4]           # short tons
    
    final_scc_array[np.absolute(final_scc_array[:])<1e-8] = 0.0
    ################################################################################################

    ################################################################################################
    ### 
    headerline1   = 'SCC,TOG.AllControlled,TOG.wRules,TOG.Difference,VOC.AllControlled,VOC.wRules,VOC.Difference'
    headerline2   = 'All emissions reported in short tons/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_by_scc/'+str(year)+'/scc_totals_summary_'+str(year)+'.csv'
    np.savetxt(output_file,final_scc_array[:],delimiter=',',header=headerline)
    ################################################################################################

####################################################################################################