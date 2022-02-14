import numpy as np

####################################################################################################
### This function generates SCC-specific TOG/VOC summary csv files
####################################################################################################

####################################################################################################
def summary(year,subpuc_names,annual_pop,subpuc_scc_map,tot_population):

    ################################################################################################
    ### Import State and County spatial allocation data. 
    subpuc_state_allocation  = np.genfromtxt('./input/allocation/subpuc_state_allocation_'+str(year)+'.csv',delimiter=',',skip_header=2)  # fipstate, fipcty, count for every sub-PUC
    scc_state_allocation     = np.genfromtxt('./input/allocation/scc_state_allocation_'+str(year)+'.csv',delimiter=',',skip_header=2)     # fipstate, fipcty, count for every sub-PUC
    state_rule_scaling       = np.genfromtxt('./input/subpuc_state_scaling4rules.csv',delimiter=',',skip_header=2)    
    ### Import sub-PUC TOG emissions.
    subPUC_TOG_emis          = np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(9))    # volatile.emission.kg/person/yr
    ### Import sub-PUC VOC emissions.
    subPUC_VOC_emis          = np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(11))   # VOC.emission.kg/person/yr
    ### Import SCC TOG emissions.
    scc_TOG_emis             = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(9))    # volatile.emission.kg/person/yr
    ### Import SCC VOC emissions.
    scc_VOC_emis             = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(11))   # VOC.emission.kg/person/yr
    ### Import SCC labels.
    scc_labels               = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',dtype='str',delimiter=',',skip_header=1,usecols=(0))    # SCC
    ################################################################################################

    ################################################################################################
    ### Initialize the final arrays. 
    ### Final emissions, State-level
    final_subpuc_state_TOG_array         = np.zeros((len(subpuc_state_allocation),len(subPUC_TOG_emis)+2))
    final_subpuc_state_TOG_array[:,0:2]  = subpuc_state_allocation[:,0:2]
    final_subpuc_state_VOC_array         = np.zeros((len(subpuc_state_allocation),len(subPUC_VOC_emis)+2))
    final_subpuc_state_VOC_array[:,0:2]  = subpuc_state_allocation[:,0:2]
    final_scc_state_TOG_array            = np.zeros((len(scc_state_allocation),len(scc_TOG_emis)+2))
    final_scc_state_TOG_array[:,0:2]     = scc_state_allocation[:,0:2]
    final_scc_state_VOC_array            = np.zeros((len(scc_state_allocation),len(scc_VOC_emis)+2))
    final_scc_state_VOC_array[:,0:2]     = scc_state_allocation[:,0:2]
    ### Unctrolled emissions, State-level
    unctrl_subpuc_state_VOC_array        = np.zeros((len(subpuc_state_allocation),len(subPUC_VOC_emis)+2))
    unctrl_subpuc_state_VOC_array[:,0:2] = subpuc_state_allocation[:,0:2]
    unctrl_scc_state_VOC_array           = np.zeros((len(scc_VOC_emis)))
    ### Final emissions, SCC-level
    final_scc_array                      = np.zeros((len(scc_labels),10))
    final_scc_array[:,0]                 = scc_labels[:]
    uncrtl_population                    = np.zeros((len(subpuc_state_allocation),len(subPUC_TOG_emis)))
    ################################################################################################
    
    ################################################################################################
    for i in range(len(tot_population[0,2:])):
        if tot_population[0,2+i] == year:
            tot_population = tot_population[1:,2+i]
            break
        else: pass

    ### Calculate State-level emissions for each unspeciated sub-PUC and SCC
    subPUC_TOG_emis                     = subPUC_TOG_emis[:] * annual_pop
    subPUC_VOC_emis                     = subPUC_VOC_emis[:] * annual_pop
    scc_TOG_emis                        = scc_TOG_emis[:] * annual_pop
    scc_VOC_emis                        = scc_VOC_emis[:] * annual_pop

    total_subpuc_state_allocation       = np.sum(subpuc_state_allocation[:,2:],axis=0)
    subpuc_state_allocation[:,2:]       = subpuc_state_allocation[:,2:]  / total_subpuc_state_allocation[:]

    for i in range(len(state_rule_scaling)):
        target_state = state_rule_scaling[i,0]
        for j in range(len(final_subpuc_state_TOG_array)):
            if final_subpuc_state_TOG_array[j,0] == target_state:
                final_subpuc_state_TOG_array[j,2:]  = subpuc_state_allocation[j,2:] * subPUC_TOG_emis[:] * state_rule_scaling[i,2:]
                final_subpuc_state_VOC_array[j,2:]  = subpuc_state_allocation[j,2:] * subPUC_VOC_emis[:] * state_rule_scaling[i,2:]
            else: pass

    for i in range(len(scc_labels)):
        for j in range(len(subpuc_scc_map)):
            if scc_labels[i] == subpuc_scc_map[j,0]:
                for k in range(len(subpuc_names)):
                    if subpuc_names[k] == subpuc_scc_map[j,1]:
                        final_scc_state_TOG_array[:,2+i]   += final_subpuc_state_TOG_array[:,2+k]
                        final_scc_state_VOC_array[:,2+i]   += final_subpuc_state_VOC_array[:,2+k]
                        break
                    else: pass
            else: pass

    state_rule_scaling[state_rule_scaling[:]==1.0] = 0.0
    state_rule_scaling[state_rule_scaling[:]>1.0]  = 1.0
    
    for i in range(len(state_rule_scaling)):
        for j in range(len(state_rule_scaling[0,2:])):
            if state_rule_scaling[i,2+j] == 0:
                uncrtl_population[i,j] = 0
            else:
                uncrtl_population[i,j] = tot_population[i]

    unctrl_subpuc_state_VOC_array[:,2:] = final_subpuc_state_VOC_array[:,2:] * state_rule_scaling[:,2:] * 2.20462
    
    for i in range(len(scc_labels)):
        for j in range(len(subpuc_scc_map)):
            if scc_labels[i] == subpuc_scc_map[j,0]:
                for k in range(len(subpuc_names)):
                    if subpuc_names[k] == subpuc_scc_map[j,1]:
                        if np.sum(uncrtl_population[:,k],axis=0) == 0:
                            unctrl_scc_state_VOC_array[i] = 0.0
                        else:
                            unctrl_scc_state_VOC_array[i] += np.sum(unctrl_subpuc_state_VOC_array[:,2+k],axis=0) / np.sum(uncrtl_population[:,k],axis=0)
                            break
                    else: pass
            else: pass

    unctrl_scc_state_VOC_array[unctrl_scc_state_VOC_array[:]<=0.0] = np.nan

    ###
    final_scc_array[:,1]                = scc_TOG_emis[:] * 0.00110231                                  # short tons
    final_scc_array[:,2]                = np.sum(final_scc_state_TOG_array[:,2:],axis=0) * 0.00110231   # short tons
    final_scc_array[:,3]                = final_scc_array[:,2] - final_scc_array[:,1]                   # short tons
    final_scc_array[:,4]                = scc_VOC_emis[:] * 0.00110231                                  # short tons
    final_scc_array[:,5]                = np.sum(final_scc_state_VOC_array[:,2:],axis=0) * 0.00110231   # short tons
    final_scc_array[:,6]                = final_scc_array[:,5] - final_scc_array[:,4]                   # short tons
    final_scc_array[:,7]                = final_scc_array[:,4] * 2000 / annual_pop                      # lb/person/yr
    final_scc_array[:,8]                = unctrl_scc_state_VOC_array[:]                                 # lb/person/yr
    final_scc_array[:,9]                = final_scc_array[:,8] / final_scc_array[:,7]                   # ratio
    
    final_scc_array[np.absolute(final_scc_array[:])<1e-8] = 0.0
    ################################################################################################

    ################################################################################################
    ### 
    headerline    = 'SCC,TOG.AllControlled.ShortTons,TOG.wRules.ShortTons,TOG.Difference.ShortTons,VOC.AllControlled.ShortTons,VOC.wRules.ShortTons,VOC.Difference.ShortTons,ControlledVOC.EF.lb/person/yr,UncontrolledVOC.EF.lb/person/yr,UncontrolledEF.Multiplier'
    output_file   = './output/emissions_by_scc/'+str(year)+'/scc_totals_summary_'+str(year)+'.csv'
    np.savetxt(output_file,final_scc_array[:],delimiter=',',header=headerline)
    ################################################################################################

####################################################################################################