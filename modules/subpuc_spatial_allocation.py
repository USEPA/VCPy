import sys
import numpy as np
import pandas as pd
from datetime import datetime

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
    subpuc_state_allocation  = np.genfromtxt('./input/allocation/subpuc_state_allocation_'+str(year)+'.csv',delimiter=',',skip_header=2)  # fipstate, fipcty, count for every sub-PUC
    subpuc_county_allocation = np.genfromtxt('./input/allocation/subpuc_county_allocation_'+str(year)+'.csv',delimiter=',',skip_header=2) # fipstate, fipcty, count for every sub-PUC
    state_subpucs            = np.genfromtxt('./input/allocation/subpuc_state_allocation_'+str(year)+'.csv',delimiter=',',dtype='str')
    county_subpucs           = np.genfromtxt('./input/allocation/subpuc_county_allocation_'+str(year)+'.csv',delimiter=',',dtype='str')
    scc_state_allocation     = np.genfromtxt('./input/allocation/scc_state_allocation_'+str(year)+'.csv',delimiter=',',skip_header=2)     # fipstate, fipcty, count for every sub-PUC
    scc_county_allocation    = np.genfromtxt('./input/allocation/scc_county_allocation_'+str(year)+'.csv',delimiter=',',skip_header=2)    # fipstate, fipcty, count for every sub-PUC
    state_scc                = np.genfromtxt('./input/allocation/scc_state_allocation_'+str(year)+'.csv',delimiter=',',dtype='str')     
    county_scc               = np.genfromtxt('./input/allocation/scc_county_allocation_'+str(year)+'.csv',delimiter=',',dtype='str')    
    ### Import sub-PUC TOG emissions.
    subPUC_TOG_emis          = np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(7))    # volatile.emission.kg/person/yr
    ### Import sub-PUC VOC emissions.
    subPUC_VOC_emis          = np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(9))    # VOC.emission.kg/person/yr
    ### Import SCC TOG emissions.
    scc_TOG_emis             = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(7))    # volatile.emission.kg/person/yr
    ### Import SCC VOC emissions.
    scc_VOC_emis             = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(9))    # VOC.emission.kg/person/yr
    ### Import SCC labels.
    scc_labels               = np.genfromtxt('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv',dtype='str',delimiter=',',skip_header=1,usecols=(0))    # SCC
    ################################################################################################

    ################################################################################################
    ### Check order of allocation arrays.
    if np.array_equal(county_subpucs[0,2:],subpuc_names[:]):
        pass
    else: sys.exit('There is an issue with your subpuc_county_allocation_YYYY.csv file. sub-PUCs in wrong order.')
    if np.array_equal(state_subpucs[0,2:],subpuc_names[:]):
        pass
    else: sys.exit('There is an issue with your subpuc_state_allocation_YYYY.csv file. sub-PUCs in wrong order.')
    ################################################################################################

    ################################################################################################
    ### Initialize the final arrays. 
    ### Final emissions, State-level [Gg/year]
    final_subpuc_state_TOG_array         = np.zeros((len(subpuc_state_allocation),len(subPUC_TOG_emis)+2))
    final_subpuc_state_TOG_array[:,0:2]  = subpuc_state_allocation[:,0:2]
    final_subpuc_state_VOC_array         = np.zeros((len(subpuc_state_allocation),len(subPUC_VOC_emis)+2))
    final_subpuc_state_VOC_array[:,0:2]  = subpuc_state_allocation[:,0:2]
    final_scc_state_TOG_array            = np.zeros((len(scc_state_allocation),len(scc_TOG_emis)+2))
    final_scc_state_TOG_array[:,0:2]     = scc_state_allocation[:,0:2]
    final_scc_state_VOC_array            = np.zeros((len(scc_state_allocation),len(scc_VOC_emis)+2))
    final_scc_state_VOC_array[:,0:2]     = scc_state_allocation[:,0:2]
    ### Final emissions, County-level [kg/year]
    final_subpuc_county_TOG_array        = np.zeros((len(subpuc_county_allocation),len(subPUC_TOG_emis)+2))
    final_subpuc_county_TOG_array[:,0:2] = subpuc_county_allocation[:,0:2]
    final_subpuc_county_VOC_array        = np.zeros((len(subpuc_county_allocation),len(subPUC_VOC_emis)+2))
    final_subpuc_county_VOC_array[:,0:2] = subpuc_county_allocation[:,0:2]
    final_scc_county_TOG_array           = np.zeros((len(scc_county_allocation),len(scc_TOG_emis)+2))
    final_scc_county_TOG_array[:,0:2]    = scc_county_allocation[:,0:2]
    final_scc_county_VOC_array           = np.zeros((len(scc_county_allocation),len(scc_VOC_emis)+2))
    final_scc_county_VOC_array[:,0:2]    = scc_county_allocation[:,0:2]
    ################################################################################################

    ################################################################################################
    ### Calculate State-level and County-level emissions for each unspeciated sub-PUC and SCC
    subPUC_TOG_emis                     = subPUC_TOG_emis[:] * annual_pop
    subPUC_VOC_emis                     = subPUC_VOC_emis[:] * annual_pop
    scc_TOG_emis                        = scc_TOG_emis[:] * annual_pop
    scc_VOC_emis                        = scc_VOC_emis[:] * annual_pop

    total_subpuc_state_allocation       = np.sum(subpuc_state_allocation[:,2:],axis=0)
    total_subpuc_county_allocation      = np.sum(subpuc_county_allocation[:,2:],axis=0)
    total_scc_state_allocation          = np.sum(scc_state_allocation[:,2:],axis=0)
    total_scc_county_allocation         = np.sum(scc_county_allocation[:,2:],axis=0)

    subpuc_state_allocation[:,2:]       = subpuc_state_allocation[:,2:]  / total_subpuc_state_allocation[:]
    subpuc_county_allocation[:,2:]      = subpuc_county_allocation[:,2:] / total_subpuc_county_allocation[:]
    scc_state_allocation[:,2:]          = scc_state_allocation[:,2:]  / total_scc_state_allocation[:]
    scc_county_allocation[:,2:]         = scc_county_allocation[:,2:] / total_scc_county_allocation[:]

    final_subpuc_state_TOG_array[:,2:]  = subpuc_state_allocation[:,2:]  * subPUC_TOG_emis[:] / 1e6
    final_subpuc_county_TOG_array[:,2:] = subpuc_county_allocation[:,2:] * subPUC_TOG_emis[:]
    final_subpuc_state_VOC_array[:,2:]  = subpuc_state_allocation[:,2:]  * subPUC_VOC_emis[:] / 1e6
    final_subpuc_county_VOC_array[:,2:] = subpuc_county_allocation[:,2:] * subPUC_VOC_emis[:]
    
    for i in range(len(scc_labels)):
        for j in range(len(state_scc[0,2:])):
            if scc_labels[i] == state_scc[0,2+j]:
                final_scc_state_TOG_array[:,2+i]  = scc_state_allocation[:,2+j]  * scc_TOG_emis[i] / 1e6
                final_scc_state_VOC_array[:,2+i]  = scc_state_allocation[:,2+j]  * scc_VOC_emis[i] / 1e6
                break
            else: pass
        for j in range(len(county_scc[0,2:])):
            if scc_labels[i] == county_scc[0,2+j]:
                final_scc_county_TOG_array[:,2+i] = scc_county_allocation[:,2+j]  * scc_TOG_emis[i]
                final_scc_county_VOC_array[:,2+i] = scc_county_allocation[:,2+j]  * scc_VOC_emis[i]
                break
            else: pass

    print("Total National VCP Emissions [Tg/year]: ",np.round(np.nansum(subPUC_TOG_emis[:])/1e9,2))
#    print("Total National VCP Emissions [Tg/year]: ",np.round(np.nansum(final_subpuc_state_TOG_array[:,2:])/1e3,2))
#    print("Total National VCP Emissions [Tg/year]: ",np.round(np.nansum(scc_TOG_emis[:])/1e9,2))
#    print("Total National VCP Emissions [Tg/year]: ",np.round(np.nansum(final_scc_state_TOG_array[:,2:])/1e3,2))
    ################################################################################################

    ################################################################################################
    ### 
    headerline1   = 'fipstate,fipscty,'+np.array2string(subpuc_names[:],max_line_width=1e6,separator=',') 
    headerline2   = 'All emissions reported in Gg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/subpuc_state_TOG_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_subpuc_state_TOG_array[:],delimiter=',',header=headerline)
    ################################################################################################

    ################################################################################################
    ###
    headerline1   = 'fipstate,fipscty,'+np.array2string(subpuc_names[:],max_line_width=1e6,separator=',') 
    headerline2   = 'All emissions reported in kg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/subpuc_county_TOG_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_subpuc_county_TOG_array[:],delimiter=',',header=headerline)
    ################################################################################################

    ################################################################################################
    ### 
    headerline1   = 'fipstate,fipscty,'+np.array2string(subpuc_names[:],max_line_width=1e6,separator=',') 
    headerline2   = 'All emissions reported in Gg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/subpuc_state_VOC_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_subpuc_state_VOC_array[:],delimiter=',',header=headerline)
    ################################################################################################

    ################################################################################################
    ###
    headerline1   = 'fipstate,fipscty,'+np.array2string(subpuc_names[:],max_line_width=1e6,separator=',') 
    headerline2   = 'All emissions reported in kg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/subpuc_county_VOC_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_subpuc_county_VOC_array[:],delimiter=',',header=headerline)
    ################################################################################################

    ################################################################################################
    ### 
    temp          = ','.join(map(str,scc_labels[:]))
    headerline1   = 'fipstate,fipscty,'+temp
    headerline2   = '# All emissions reported in Gg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/scc_state_TOG_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_scc_state_TOG_array[:],delimiter=',',header=headerline,comments='')
    ################################################################################################

    ################################################################################################
    ###
    temp          = ','.join(map(str,scc_labels[:]))
    headerline1   = 'fipstate,fipscty,'+temp
    headerline2   = '# All emissions reported in kg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/scc_county_TOG_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_scc_county_TOG_array[:],delimiter=',',header=headerline,comments='')
    ################################################################################################

    ################################################################################################
    ### 
    temp          = ','.join(map(str,scc_labels[:]))
    headerline1   = 'fipstate,fipscty,'+temp
    headerline2   = '# All emissions reported in Gg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/scc_state_VOC_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_scc_state_VOC_array[:],delimiter=',',header=headerline,comments='')
    ################################################################################################

    ################################################################################################
    ###
    temp          = ','.join(map(str,scc_labels[:]))
    headerline1   = 'fipstate,fipscty,'+temp
    headerline2   = '# All emissions reported in kg/year'
    headerline    = '\n'.join([headerline1,headerline2])
    output_file   = './output/emissions_spatially_allocated/'+str(year)+'/scc_county_VOC_emissions_'+str(year)+'.csv'
    np.savetxt(output_file,final_scc_county_VOC_array[:],delimiter=',',header=headerline,comments='')
    ################################################################################################

####################################################################################################
def smoke_flat_file(year):

    ################################################################################################
    ### Import County emissions data by SCC. 
    #### Get input dataset.
    scc_county_emissions = pd.read_csv('./output/emissions_spatially_allocated/'+str(year)+'/scc_county_VOC_emissions_'+str(year)+'.csv',delimiter=',',header=0)#,skiprows=2)
    ### Import SCC labels.
    scc_labels           = pd.read_csv('./output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv')
    scc_labels           = pd.DataFrame({'SCC': scc_labels.iloc[:,0]})
    ################################################################################################
    
    ################################################################################################
    ### Generate data.
    df = pd.DataFrame(columns=['COUNTRY_CD','REGION_CD','SCC','POLL','ANN_VALUE','CALC_YEAR','DATE_UPDATED','DATA_SET_ID','NOTE'])
    now   = datetime.now()
    for idx1, row1 in scc_county_emissions.iterrows():
        if np.isnan(row1['2461030999']):
            pass
        else:
            if float(row1['fipstate']) / 10 < 1.0:
                statefips = '0'+str(int(float(row1['fipstate'])))
            else:
                statefips = str(int(float(row1['fipstate'])))
            if float(row1['fipscty']) / 10 < 1.0:
                countyfips = '00'+str(int(float(row1['fipscty'])))
            elif float(row1['fipscty']) / 100 < 1.0 and float(row1['fipscty']) / 10 > 1.0:
                countyfips = '0'+str(int(float(row1['fipscty'])))
            else:
                countyfips = str(int(float(row1['fipscty'])))
            for idx2, row2 in scc_labels.iterrows():
                if row1[str(row2['SCC'])] == 0.0:
                    pass
                else:
                    temp_array = pd.Series(data={'COUNTRY_CD':'US','REGION_CD':statefips+countyfips,
                                                 'SCC':row2['SCC'],'POLL':'VOC','ANN_VALUE':row1[str(row2['SCC'])]*0.00110231,
                                                 'CALC_YEAR':str(year),'DATE_UPDATED':now.strftime('%Y%m%d'),
                                                 'DATA_SET_ID':'VCPy_'+str(year),'NOTE':'No Point Source Subtraction'})
                    df = df.append(temp_array,ignore_index=True)

    ################################################################################################
    ### Output
    df.to_csv('./output/smoke_flat_file/'+str(year)+'/VCPy_SmokeFlatFile_'+str(year)+'.csv',index=False)
    ################################################################################################

####################################################################################################