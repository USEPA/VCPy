import numpy as np

####################################################################################################
### These functions collectively calculate the total and speciated emissions for all sub-PUCs.
####################################################################################################

####################################################################################################
def calc_evaptime(d,ve,chem_props_vars):
    evaptime = (10**chem_props_vars[:,4]) * (d / 1000) / ve
    return evaptime
####################################################################################################

####################################################################################################
def calc_c_mass(chem_props_vars):
    c_mass = chem_props_vars[:,1] * 12.0 / chem_props_vars[:,3]
    return c_mass
####################################################################################################

####################################################################################################
def year_specific_usage(year,subpuc_usage):
    for i in range(len(subpuc_usage[0,1:])):
        if subpuc_usage[0,1+i] == year:
            target_usage = subpuc_usage[1:,1+i]
        else: pass
    return target_usage
####################################################################################################

####################################################################################################
def calc_subpuc_emis(year,subpuc_names,year_specific_usage,subpuc_usetime,subpuc_controls,first_ord_spec,organic_spec,\
                     chem_props_vars,chem_props_strs,evaptime,c_mass,subpuc_scc_map):

    ################################################################################################
    ### Timescale thresholds. [seconds, minutes, hours, days, weeks, months, years]
    thresholds       = np.array((2.778E-04, 1.667E-02, 1.000E+00, 2.400E+01, 1.680E+02, 7.200E+02, 8.760E+03))
    ################################################################################################

    unique_scc       = np.unique(subpuc_scc_map[:,0])

    ################################################################################################
    ### Initialize the final arrays. 
    ### Final emissions per sub-PUC per compound [kg/person/year]
    final_subPUC_emissions = np.zeros((len(chem_props_vars),len(subpuc_names)))
    ### Final emissions per SCC per compound [kg/person/year]
    final_SCC_emissions    = np.zeros((len(chem_props_vars),len(unique_scc)))
    ### Final emissions per sub-PUC per compound [kgC/person/year]
    carbon_emissions       = np.zeros((len(chem_props_vars),len(subpuc_names)))
    ### VOC emissions per sub-PUC per compound [kg/person/year]
    voc_emissions          = np.zeros((len(chem_props_vars),len(subpuc_names)))
    ### Final sub-PUC summary array
    final_subPUC_summary   = np.zeros((len(subpuc_names),14))
    ### Final SCC summary array
    final_SCC_summary      = np.zeros((len(unique_scc),14))
    ################################################################################################

    ################################################################################################
    ### Calculate emissions per sub-PUC per compound [kg/person/year]
    for i in range(len(subpuc_names)):                 # loop for each sub-PUC
        for j in range(len(chem_props_vars)):          # loop for each chemical
            if evaptime[j] <= thresholds[int(subpuc_usetime[i,1])]:
                final_subPUC_emissions[j,i]  = organic_spec[1+j,i] * year_specific_usage[i] * first_ord_spec[i,3] * (1 - subpuc_controls[i,1])
                carbon_emissions[j,i] = organic_spec[1+j,i] * year_specific_usage[i] * first_ord_spec[i,3] * (1 - subpuc_controls[i,1]) * c_mass[j]
            else: pass

    final_subPUC_emissions[np.isnan(final_subPUC_emissions[:,:])] = 0.0
    carbon_emissions[np.isnan(carbon_emissions[:,:])] = 0.0

    ### Create emissions array per SCC per compound [kg/person/year]    
    for i in range(len(unique_scc)):
        for j in range(len(subpuc_scc_map)):
            if unique_scc[i] == subpuc_scc_map[j,0]:
                target_subPUC = subpuc_scc_map[j,1]
                for k in range(len(subpuc_names)):
                    if target_subPUC == subpuc_names[k]:
                        final_SCC_emissions[:,i] += final_subPUC_emissions[:,k]
                    else: pass

    print('Year: '+str(year))
    print("Total [kg/person/year]: ",np.round(np.nansum(final_subPUC_emissions[:,:]),3))
    ################################################################################################

    ################################################################################################
    ### Calculate effective SOA Yields and MIR for each sub-PUC and SCC
    subpuc_emis_perc = np.zeros((len(chem_props_vars),len(subpuc_names)))
    scc_emis_perc    = np.zeros((len(chem_props_vars),len(unique_scc)))
    SOA_Yield_subpuc = np.zeros(len(subpuc_names))
    MIR_subpuc       = np.zeros(len(subpuc_names))
    SOA_Yield_scc    = np.zeros(len(unique_scc))
    MIR_scc          = np.zeros(len(unique_scc))

    subpuc_emis_perc[:,:] = final_subPUC_emissions[:,:] / np.nansum(final_subPUC_emissions[:,:],axis=0)
    scc_emis_perc[:,:]    = final_SCC_emissions[:,:] / np.nansum(final_SCC_emissions[:,:],axis=0)

    for i in range(len(subpuc_names)):
        SOA_Yield_subpuc[i]   = np.nansum(subpuc_emis_perc[:,i] * chem_props_vars[:,6])
        MIR_subpuc[i]         = np.nansum(subpuc_emis_perc[:,i] * chem_props_vars[:,7])
    for i in range(len(unique_scc)):
        SOA_Yield_scc[i]      = np.nansum(scc_emis_perc[:,i] * chem_props_vars[:,6])
        MIR_scc[i]            = np.nansum(scc_emis_perc[:,i] * chem_props_vars[:,7])
    ################################################################################################

    ################################################################################################
    ### Filter nonVOCTOG to get total VOC emissions.
    for i in range(len(final_subPUC_emissions)):
        if chem_props_strs[i,2] == 'FALSE':
            voc_emissions[i,:] = final_subPUC_emissions[i,:]
        else:
            voc_emissions[i,:] = 0.0
    ################################################################################################

    ################################################################################################
    ### Calculate summary statistics
    final_subPUC_summary[:,0]   = year_specific_usage[:]
    final_subPUC_summary[:,1]   = year_specific_usage[:] * first_ord_spec[:,0]
    final_subPUC_summary[:,2]   = year_specific_usage[:] * first_ord_spec[:,1]
    final_subPUC_summary[:,3]   = year_specific_usage[:] * first_ord_spec[:,2]
    final_subPUC_summary[:,4]   = year_specific_usage[:] * (first_ord_spec[:,2] - first_ord_spec[:,3])
    final_subPUC_summary[:,5]   = year_specific_usage[:] * first_ord_spec[:,3]
    final_subPUC_summary[:,6]   = np.nansum(final_subPUC_emissions[:,:],axis=0)
    final_subPUC_summary[:,7]   = np.nansum(carbon_emissions[:,:],axis=0)
    final_subPUC_summary[:,8]   = np.nansum(voc_emissions[:,:],axis=0)
    final_subPUC_summary[:,9]   = np.round(final_subPUC_summary[:,6] / final_subPUC_summary[:,5],4)
    final_subPUC_summary[:,10]  = np.round(final_subPUC_summary[:,6] / final_subPUC_summary[:,3],4)
    final_subPUC_summary[:,11]  = np.round(final_subPUC_summary[:,6] / final_subPUC_summary[:,0],4)
    final_subPUC_summary[:,12]  = SOA_Yield_subpuc[:] * 100
    final_subPUC_summary[:,13]  = MIR_subpuc[:]

    ### Create final array per SCC 
    for i in range(len(unique_scc)):
        for j in range(len(subpuc_scc_map)):
            if unique_scc[i] == subpuc_scc_map[j,0]:
                target_subPUC = subpuc_scc_map[j,1]
                for k in range(len(subpuc_names)):
                    if target_subPUC == subpuc_names[k]:
                        final_SCC_summary[i,0:9] += final_subPUC_summary[k,0:9]
                    else: pass
    final_SCC_summary[:,9]   = np.round(final_SCC_summary[:,6] / final_SCC_summary[:,5],4)
    final_SCC_summary[:,10]  = np.round(final_SCC_summary[:,6] / final_SCC_summary[:,3],4)
    final_SCC_summary[:,11]  = np.round(final_SCC_summary[:,6] / final_SCC_summary[:,0],4)
    final_SCC_summary[:,12]  = SOA_Yield_scc[:] * 100
    final_SCC_summary[:,13]  = MIR_scc[:]
    ################################################################################################

    ################################################################################################
    ### Generate a per sub-PUC summary output file.
    headerline1   = 'sub-PUC,totaluse.kg/person/yr,water.kg/person/yr,inorganic.kg/person/yr,organic.kg/person/yr,nonvolatile.kg/person/yr,volatile.kg/person/yr,volatile.emission.kg/person/yr,volatile.emission.kgC/person/yr,VOC.emission.kg/person/yr,%volatile.emitted,%organic.emitted,%product.emitted,SOAYield.%,MIR.gO3/g'
    output_file   = './output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv'
    np.savetxt(output_file,np.column_stack((subpuc_names[:],final_subPUC_summary[:])),delimiter=',',fmt='%s',header=headerline1)

    ### Generate a per SCC summary output file.
    headerline1   = 'SCC,totaluse.kg/person/yr,water.kg/person/yr,inorganic.kg/person/yr,organic.kg/person/yr,nonvolatile.kg/person/yr,volatile.kg/person/yr,volatile.emission.kg/person/yr,volatile.emission.kgC/person/yr,VOC.emission.kg/person/yr,%volatile.emitted,%organic.emitted,%product.emitted,SOAYield.%,MIR.gO3/g'
    output_file   = './output/emissions_by_scc/'+str(year)+'/summary_by_scc_'+str(year)+'.csv'
    np.savetxt(output_file,np.column_stack((unique_scc[:],final_SCC_summary[:])),delimiter=',',fmt='%s',header=headerline1)

    ### Generate a speciated per sub-PUC output file.
    headerline1   = np.array2string(subpuc_names[:],max_line_width=1e6,separator=',')
    output_file   = './output/emissions_by_subpuc/'+str(year)+'/speciated_emissions_by_subpuc_'+str(year)+'.csv'
    np.savetxt(output_file,final_subPUC_emissions[:,:],delimiter=',',header=headerline1)
####################################################################################################