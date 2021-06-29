import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams, cm

####################################################################################################
### These functions generate summary figures.
####################################################################################################

####################################################################################################
####
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams['font.size'] = 18
####
####################################################################################################

####################################################################################################
def check_create_directory(loopsubpucs):
    try:
        os.makedirs('./output/figures/'+str(loopsubpucs))
    except FileExistsError:
        pass
####################################################################################################

####################################################################################################
def subpuc_timeseries(loopsubpucs,years2loop):

    ################################################################################################
    #### Final sub-PUC array
    subpuc_array = np.zeros((len(years2loop)))
    ################################################################################################

    counter = 0
    for year in years2loop:

        ############################################################################################
        ### Import data.
        temp_array = np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(7))
        name_array = np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,dtype='str',usecols=(0))
        ############################################################################################
        
        for i in range(len(name_array)):
            if name_array[i] == loopsubpucs:
                subpuc_array[counter] = temp_array[i]
            else: pass
        counter += 1
    return subpuc_array
####################################################################################################

####################################################################################################
def population_timeseries(years2loop):

    ################################################################################################
    ### Import data.
    tot_population   = np.genfromtxt("./input/state_population.csv",delimiter=",")
    ################################################################################################

    ################################################################################################
    #### Final population array
    population_array = np.zeros((len(years2loop)))
    ################################################################################################
    
    for i in range(len(population_array)):
        for j in range(len(tot_population[0,2:])):
            if tot_population[0,2+j] == years2loop[i]:
                population_array[i] = np.sum(tot_population[1:,2+j])
            else: pass
    return population_array
####################################################################################################

####################################################################################################
def percap_timeseries(loopsubpucs,years2loop,subpuc_array):
    
    fig         = plt.figure(figsize=(6,4),frameon=False)
    line_plt   = fig.add_axes([0.14,0.12,0.76,0.76])
    
    line_plt.plot(years2loop[:],subpuc_array[:],'#525252',label=loopsubpucs,linewidth=4)
    
    line_plt.legend(loc=1,numpoints=1,ncol=2,fontsize=8,framealpha=1.0)
    line_plt.axis([years2loop[0],years2loop[-1],0,np.max(subpuc_array[:])*1.2])
    line_plt.set_xlabel('Year',fontsize=10)
    line_plt.set_ylabel('Emissions [kg person$^{-1}$ year$^{-1}$]',fontsize=10)
    line_plt.tick_params(labelsize=10)
    line_plt.yaxis.grid(True,linestyle='--',which='major',color='k',alpha=0.5,zorder=0)
    
    plt.savefig('./output/figures/'+str(loopsubpucs)+'/'+str(loopsubpucs)+'_percap_timeseries.pdf')
####################################################################################################

####################################################################################################
def mass_timeseries(loopsubpucs,years2loop,subpuc_array,population_array):
    
    plot_array = subpuc_array[:] * population_array[:] / 1e6
    
    fig         = plt.figure(figsize=(6,4),frameon=False)
    line_plt   = fig.add_axes([0.14,0.12,0.76,0.76])
    
    line_plt.plot(years2loop[:],plot_array[:],'#525252',label=loopsubpucs,linewidth=4)
    
    line_plt.legend(loc=1,numpoints=1,ncol=2,fontsize=8,framealpha=1.0)
    line_plt.axis([years2loop[0],years2loop[-1],0,np.max(plot_array[:])*1.2])
    line_plt.set_xlabel('Year',fontsize=10)
    line_plt.set_ylabel('Emissions [Gg year$^{-1}$]',fontsize=10)
    line_plt.tick_params(labelsize=10)
    line_plt.yaxis.grid(True,linestyle='--',which='major',color='k',alpha=0.5,zorder=0)
    
    plt.savefig('./output/figures/'+str(loopsubpucs)+'/'+str(loopsubpucs)+'_mass_timeseries.pdf')
####################################################################################################

####################################################################################################
def vol_distribution(years2loop,chem_props_vars,chem_props_strs,loopsubpucs,subpuc_names):
    
    ################################################################################################
    ### Import data from ENDYEAR.
    organic_spec     = np.genfromtxt('./output/emissions_by_subpuc/'+str(years2loop[-1])+'/speciated_emissions_by_subpuc_'+str(years2loop[-1])+'.csv',delimiter=',',skip_header=1)
    ################################################################################################

    ################################################################################################
    for i in range(len(subpuc_names)):
        if subpuc_names[i] == loopsubpucs:
            organic_spec  = organic_spec[:,i]
            break
        else: pass

    vol_bin_nums  = np.arange(1,11,1)
    vol_dist      = np.zeros((len(vol_bin_nums),2))
    vol_dist[:,0] = vol_bin_nums[:]
    
    for i in range(len(organic_spec)):
        for j in range(len(vol_dist)):
            if j == 0:
               if chem_props_vars[i,5] < (vol_dist[j+1,0] - 0.5):
                  vol_dist[j,1] = vol_dist[j,1] + organic_spec[i]
               else: pass
            elif j == len(vol_dist)-1:
               if chem_props_vars[i,5] >= (vol_dist[j,0] - 0.5):
                  vol_dist[j,1] = vol_dist[j,1] + organic_spec[i]
               else: pass
            else:
               if (chem_props_vars[i,5] < (vol_dist[j+1,0] - 0.5)) and (chem_props_vars[i,5] >= (vol_dist[j,0] - 0.5)):
                  vol_dist[j,1] = vol_dist[j,1] + organic_spec[i]
               else: pass
    ################################################################################################

    vol_dist[:] = vol_dist[:] * 1000

    ################################################################################################

    ################################################################################################
    fig      = plt.figure(figsize=(7,4),frameon=False)
    bar_plt  = fig.add_axes([0.12,0.14,0.86,0.78])

    opacity   = 1 
    labels = ['1','2','3','4','5','6','7','8','9','10+']

    x      = np.arange(len(labels))
    width  = 0.80

    bar_plt.bar([0.25,0.25],[0,1e9],width=2.5,color='#a1d99b',zorder=1,alpha=0.3)
    bar_plt.bar([3.5,3.5],[0,1e9],width=4.0,color='#bcbddc',zorder=1,alpha=0.3)

    bar_plt.plot([1.5,1.5],[0,1e9],color='#bdbdbd',linestyle='--',linewidth=0.5)
    bar_plt.plot([5.5,5.5],[0,1e9],color='#bdbdbd',linestyle='--',linewidth=0.5)

    bar_plt.bar(x[:],vol_dist[:,1],width,color='#662506',zorder=2)

    max_val = np.max(vol_dist[:,1])*1.5

    bar_plt.axis([x[0]-width*0.75,x[-1]+width*0.75,0,max_val])
    bar_plt.set_xticks(x)
    bar_plt.set_xticklabels(labels)
    bar_plt.set_yticks([0,int(max_val*1/4),int(max_val*2/4),int(max_val*3/4),int(max_val*4/4)])
    bar_plt.set_ylabel('Emissions [g person$^{-1}$ year$^{-1}$]',fontsize=14)
    bar_plt.set_xlabel('log$_{10}$C*',fontsize=14)
    bar_plt.tick_params(labelsize=12)
    bar_plt.yaxis.grid(True,linestyle='--',which='major',color='k',alpha=0.5,zorder=1)
    bar_plt.tick_params(axis='x',which='both',bottom='off',top='off')
    bar_plt.tick_params(axis='y',which='both',left='on',right='off')
    bar_plt.set_title(loopsubpucs,fontsize=16)

    fig.text(.18, .88, 'SVOC', fontsize=12, color='k')
    fig.text(.435, .88, 'IVOC', fontsize=12, color='k')
    fig.text(.785, .88, 'VOC', fontsize=12, color='k')

    plt.savefig('./output/figures/'+str(loopsubpucs)+'/'+str(loopsubpucs)+'_vol_distribution.pdf')
    plt.savefig('./output/figures/'+str(loopsubpucs)+'/'+str(loopsubpucs)+'_vol_distribution.png',dpi=400)
####################################################################################################

####################################################################################################
def total_timeseries(years2loop):
    
    final_array = np.zeros((len(years2loop)))
    counter      = 0
    
    for year in years2loop:

        ############################################################################################
        ### Import data.
        final_array[counter] = np.sum(np.genfromtxt('./output/emissions_by_subpuc/'+str(year)+'/summary_by_subpuc_'+str(year)+'.csv',delimiter=',',skip_header=1,usecols=(7)))
        ############################################################################################
        
        counter += 1
    return final_array
####################################################################################################

####################################################################################################
def total_percap_timeseries(years2loop,total_array):
    
    fig         = plt.figure(figsize=(6,4),frameon=False)
    line_plt   = fig.add_axes([0.10,0.12,0.76,0.76])

    line_plt.plot(years2loop[:],total_array[:],'#525252',label='TOTAL',linewidth=4)

    line_plt.legend(loc=1,numpoints=1,ncol=2,fontsize=8,framealpha=1.0)
    line_plt.axis([years2loop[0],years2loop[-1],np.min(total_array[:])*0.6,np.max(total_array[:])*1.2])
    line_plt.set_xlabel('Year',fontsize=10)
    line_plt.set_ylabel('Emissions [kg person$^{-1}$ year$^{-1}$]',fontsize=10)
    line_plt.tick_params(labelsize=10)
    line_plt.yaxis.grid(True,linestyle='--',which='major',color='k',alpha=0.5,zorder=0)

    plt.savefig('./output/figures/TOTAL_percapita_timeseries.pdf')
####################################################################################################

####################################################################################################
def total_mass_timeseries(years2loop,total_array,population_array):
    
    plot_array = total_array[:] * population_array[:] / 1e9

    fig         = plt.figure(figsize=(6,4),frameon=False)
    line_plt   = fig.add_axes([0.14,0.12,0.76,0.76])
    
    line_plt.plot(years2loop[:],plot_array[:],'#525252',label='TOTAL',linewidth=4)
    
    line_plt.legend(loc=1,numpoints=1,ncol=2,fontsize=8,framealpha=1.0)
    line_plt.axis([years2loop[0],years2loop[-1],np.min(plot_array[:])*0.6,np.max(plot_array[:])*1.2])
    line_plt.set_xlabel('Year',fontsize=10)
    line_plt.set_ylabel('Emissions [Tg year$^{-1}$]',fontsize=10)
    line_plt.tick_params(labelsize=10)
    line_plt.yaxis.grid(True,linestyle='--',which='major',color='k',alpha=0.5,zorder=0)
    
    plt.savefig('./output/figures/TOTAL_mass_timeseries.pdf')
####################################################################################################

####################################################################################################
def findgroup_wOCsplit(group_name,OC_ratio):
    
    if group_name == 'n-alkane': group_index = 1
    elif group_name == 'b-alkane': group_index = 2
    elif group_name == 'c-alkane': group_index = 3
    elif group_name == 'aromatic': group_index = 4
    elif group_name == 'alkene': group_index = 5
    elif group_name == 'oxygenated' and OC_ratio < 0.45: group_index = 6
    elif group_name == 'oxygenated' and OC_ratio >= 0.45: group_index = 7
    elif group_name == 'halocarbon': group_index = 8
    else: group_index = 9
    
    return(group_index)
####################################################################################################

####################################################################################################
def findgroup(group_name,OC_ratio):
    
    if group_name == 'n-alkane': group_index = 1
    elif group_name == 'b-alkane': group_index = 2
    elif group_name == 'c-alkane': group_index = 3
    elif group_name == 'aromatic': group_index = 4
    elif group_name == 'alkene': group_index = 5
    elif group_name == 'oxygenated': group_index = 6
    elif group_name == 'halocarbon': group_index = 7
    else: group_index = 8
    
    return(group_index)
####################################################################################################

####################################################################################################
def total_vol_distribution_wOCsplit(years2loop,chem_props_vars,chem_props_strs):

    ################################################################################################
    ### Import data from ENDYEAR.
    organic_spec     = np.genfromtxt('./output/emissions_by_subpuc/'+str(years2loop[-1])+'/speciated_emissions_by_subpuc_'+str(years2loop[-1])+'.csv',delimiter=',',skip_header=1)
    ################################################################################################

    ################################################################################################
    organic_spec  = np.nansum(organic_spec[:,:],axis=1)

    vol_bin_nums  = np.arange(1,11,1)
    vol_dist      = np.zeros((len(vol_bin_nums),9))
    vol_dist[:,0] = vol_bin_nums[:]
    OxyCarRatio   = chem_props_vars[:,2] / chem_props_vars[:,1]
    OxyCarRatio[np.isnan(OxyCarRatio[:])] = 0.0

    for i in range(len(organic_spec)):
        for j in range(len(vol_dist)):
            if j == 0:
               if chem_props_vars[i,5] < (vol_dist[j+1,0] - 0.5):
                   group = findgroup_wOCsplit(chem_props_strs[i,0],OxyCarRatio[i])
                   if group == 9: pass
                   else: vol_dist[j,group] = vol_dist[j,group] + organic_spec[i]
               else: pass
            elif j == len(vol_dist)-1:
               if chem_props_vars[i,5] >= (vol_dist[j,0] - 0.5):
                   group = findgroup_wOCsplit(chem_props_strs[i,0],OxyCarRatio[i])
                   if group == 9: pass
                   else: vol_dist[j,group] = vol_dist[j,group] + organic_spec[i]
               else: pass
            else:
               if (chem_props_vars[i,5] < (vol_dist[j+1,0] - 0.5)) and (chem_props_vars[i,5] >= (vol_dist[j,0] - 0.5)):
                   group = findgroup_wOCsplit(chem_props_strs[i,0],OxyCarRatio[i])
                   if group == 9: pass
                   else: vol_dist[j,group] = vol_dist[j,group] + organic_spec[i]
               else: pass
    ################################################################################################

    vol_dist[:] = vol_dist[:] * 1000

    ################################################################################################
    fig      = plt.figure(figsize=(7,4),frameon=False)
    bar_plt  = fig.add_axes([0.12,0.14,0.86,0.78])

    opacity   = 1 
    labels = ['1','2','3','4','5','6','7','8','9','10+']

    x      = np.arange(len(labels))
    width  = 0.80

    bar_plt.bar([0.25,0.25],[0,1e9],width=2.5,color='#a1d99b',zorder=1,alpha=0.3)
    bar_plt.bar([3.5,3.5],[0,1e9],width=4.0,color='#bcbddc',zorder=1,alpha=0.3)

    bar_plt.plot([1.5,1.5],[0,1e9],color='#bdbdbd',linestyle='--',linewidth=0.5)
    bar_plt.plot([5.5,5.5],[0,1e9],color='#bdbdbd',linestyle='--',linewidth=0.5)

    bar_plt.bar(x[:],vol_dist[:,1],width,color='#e31a1c',label='n-Alkane',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,2],width,bottom=vol_dist[:,1],color='#fdbf6f',label='b-Alkane',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,3],width,bottom=np.sum(vol_dist[:,1:3],axis=1),color='#ffff99',label='c-Alkane',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,4],width,bottom=np.sum(vol_dist[:,1:4],axis=1),color='#6a3d9a',label='Aromatic',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,5],width,bottom=np.sum(vol_dist[:,1:5],axis=1),color='#1f78b4',label='Alkene',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,6],width,bottom=np.sum(vol_dist[:,1:6],axis=1),color='#33a02c',label='0 < O:C < 0.45',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,7],width,bottom=np.sum(vol_dist[:,1:7],axis=1),color='#b2df8a',hatch='//',label='O:C >= 0.45',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,8],width,bottom=np.sum(vol_dist[:,1:8],axis=1),color='#b15928',label='Halocarbons',zorder=2)

    max_val = 5000

    bar_plt.legend(loc=6,numpoints=1,fontsize=12,ncol=1,framealpha=1.0)
    bar_plt.axis([x[0]-width*0.75,x[-1]+width*0.75,0,max_val])
    bar_plt.set_xticks(x)
    bar_plt.set_xticklabels(labels)
    bar_plt.set_yticks([0,1250,2500,3750,5000])
    bar_plt.set_ylabel('Emissions [g person$^{-1}$ year$^{-1}$]',fontsize=14)
    bar_plt.set_xlabel('log$_{10}$C*',fontsize=14)
    bar_plt.tick_params(labelsize=12)
    bar_plt.yaxis.grid(True,linestyle='--',which='major',color='k',alpha=0.5,zorder=1)
    bar_plt.tick_params(axis='x',which='both',bottom='off',top='off')
    bar_plt.tick_params(axis='y',which='both',left='on',right='off')
    bar_plt.set_title('Total VCPs',fontsize=16)

    fig.text(.18, .88, 'SVOC', fontsize=12, color='k')
    fig.text(.435, .88, 'IVOC', fontsize=12, color='k')
    fig.text(.785, .88, 'VOC', fontsize=12, color='k')

    plt.savefig('./output/figures/TOTAL_vol_distribution.pdf')
    plt.savefig('./output/figures/TOTAL_vol_distribution.png',dpi=400)
####################################################################################################

####################################################################################################
def total_vol_distribution(years2loop,chem_props_vars,chem_props_strs):

    ################################################################################################
    ### Import data from ENDYEAR.
    organic_spec     = np.genfromtxt('./output/emissions_by_subpuc/'+str(years2loop[-1])+'/speciated_emissions_by_subpuc_'+str(years2loop[-1])+'.csv',delimiter=',',skip_header=1)
    ################################################################################################

    ################################################################################################
    organic_spec  = np.nansum(organic_spec[:,:],axis=1)

    vol_bin_nums  = np.arange(1,11,1)
    vol_dist      = np.zeros((len(vol_bin_nums),8))
    vol_dist[:,0] = vol_bin_nums[:]
    OxyCarRatio   = chem_props_vars[:,2] / chem_props_vars[:,1]
    OxyCarRatio[np.isnan(OxyCarRatio[:])] = 0.0

    for i in range(len(organic_spec)):
        for j in range(len(vol_dist)):
            if j == 0:
               if chem_props_vars[i,5] < (vol_dist[j+1,0] - 0.5):
                   group = findgroup(chem_props_strs[i,0],OxyCarRatio[i])
                   if group == 8: pass
                   else: vol_dist[j,group] = vol_dist[j,group] + organic_spec[i]
               else: pass
            elif j == len(vol_dist)-1:
               if chem_props_vars[i,5] >= (vol_dist[j,0] - 0.5):
                   group = findgroup(chem_props_strs[i,0],OxyCarRatio[i])
                   if group == 8: pass
                   else: vol_dist[j,group] = vol_dist[j,group] + organic_spec[i]
               else: pass
            else:
               if (chem_props_vars[i,5] < (vol_dist[j+1,0] - 0.5)) and (chem_props_vars[i,5] >= (vol_dist[j,0] - 0.5)):
                   group = findgroup(chem_props_strs[i,0],OxyCarRatio[i])
                   if group == 8: pass
                   else: vol_dist[j,group] = vol_dist[j,group] + organic_spec[i]
               else: pass
    ################################################################################################

    vol_dist[:] = vol_dist[:] * 1000

    ################################################################################################
    fig      = plt.figure(figsize=(7,4),frameon=False)
    bar_plt  = fig.add_axes([0.12,0.14,0.86,0.78])

    opacity   = 1 
    labels = ['1','2','3','4','5','6','7','8','9','10+']

    x      = np.arange(len(labels))
    width  = 0.80

    bar_plt.bar([0.25,0.25],[0,1e9],width=2.5,color='#a1d99b',zorder=1,alpha=0.3)
    bar_plt.bar([3.5,3.5],[0,1e9],width=4.0,color='#bcbddc',zorder=1,alpha=0.3)

    bar_plt.plot([1.5,1.5],[0,1e9],color='#bdbdbd',linestyle='--',linewidth=0.5)
    bar_plt.plot([5.5,5.5],[0,1e9],color='#bdbdbd',linestyle='--',linewidth=0.5)

    #ar_plt.bar(x[:],vol_dist[:,1],width,color='#e31a1c',label='n-Alkane',zorder=2)
    #bar_plt.bar(x[:],vol_dist[:,2],width,bottom=vol_dist[:,1],color='#fdbf6f',label='b-Alkane',zorder=2)
    #bar_plt.bar(x[:],vol_dist[:,3],width,bottom=np.sum(vol_dist[:,1:3],axis=1),color='#ffff99',label='c-Alkane',zorder=2)
    #bar_plt.bar(x[:],vol_dist[:,4],width,bottom=np.sum(vol_dist[:,1:4],axis=1),color='#6a3d9a',label='Aromatic',zorder=2)
    #bar_plt.bar(x[:],vol_dist[:,5],width,bottom=np.sum(vol_dist[:,1:5],axis=1),color='#1f78b4',label='Alkene',zorder=2)
    #bar_plt.bar(x[:],vol_dist[:,6],width,bottom=np.sum(vol_dist[:,1:6],axis=1),color='#33a02c',label='Oxygenates',zorder=2)
    #bar_plt.bar(x[:],vol_dist[:,7],width,bottom=np.sum(vol_dist[:,1:7],axis=1),color='#b15928',label='Halocarbons',zorder=2)

    bar_plt.bar(x[:],vol_dist[:,1],width,color='#ef3b2c',label='n-Alkane',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,2],width,bottom=vol_dist[:,1],color='#fd8d3c',label='b-Alkane',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,3],width,bottom=np.sum(vol_dist[:,1:3],axis=1),color='#fff7bc',label='c-Alkane',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,4],width,bottom=np.sum(vol_dist[:,1:4],axis=1),color='#807dba',label='Aromatic',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,5],width,bottom=np.sum(vol_dist[:,1:5],axis=1),color='#4292c6',label='Alkene',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,6],width,bottom=np.sum(vol_dist[:,1:6],axis=1),color='#41ab5d',label='Oxygenates',zorder=2)
    bar_plt.bar(x[:],vol_dist[:,7],width,bottom=np.sum(vol_dist[:,1:7],axis=1),color='#8c510a',label='Halocarbons',zorder=2)

    max_val = 5000

    bar_plt.legend(loc=6,numpoints=1,fontsize=12,ncol=1,framealpha=1.0)
    bar_plt.axis([x[0]-width*0.75,x[-1]+width*0.75,0,max_val])
    bar_plt.set_xticks(x)
    bar_plt.set_xticklabels(labels)
    bar_plt.set_yticks([0,1250,2500,3750,5000])
    bar_plt.set_ylabel('Emissions [g person$^{-1}$ year$^{-1}$]',fontsize=14)
    bar_plt.set_xlabel('log$_{10}$C*',fontsize=14)
    bar_plt.tick_params(labelsize=12)
    bar_plt.yaxis.grid(True,linestyle='--',which='major',color='k',alpha=0.5,zorder=1)
    bar_plt.tick_params(axis='x',which='both',bottom=True,top=False)
    bar_plt.tick_params(axis='y',which='both',left=True,right=False)
    bar_plt.set_title('Volatile Chemical Products',fontsize=16)

    fig.text(.18, .88, 'SVOC', fontsize=12, color='k')
    fig.text(.435, .88, 'IVOC', fontsize=12, color='k')
    fig.text(.785, .88, 'VOC', fontsize=12, color='k')

    plt.savefig('./output/figures/TOTAL_vol_distribution.pdf')
    plt.savefig('./output/figures/TOTAL_vol_distribution.png',dpi=400)
####################################################################################################