import numpy as np
from datetime import datetime

####################################################################################################
### Generates a composite profile.
####################################################################################################

startTime = datetime.now()

####################################################################################################
### Function to calculate per sub-PUC usage
def composite_profile(target_profile,weight):
    
    carb_profile      = profile_data[profile_data[:,0]==target_profile]
    carb_profile[:,2] = carb_profile[:,2] * weight

    return(carb_profile[:,1:])
####################################################################################################

####################################################################################################
### Import CARB profile data. 
profile_data   =  np.genfromtxt("./orgprofile18dec20.csv", delimiter=",",skip_header=1)  # PROFILE NUMBER, SAROAD, WEIGHT FRACTION
### Import CARB Bin data. 
bin_data       =  np.genfromtxt("./orgprofile_BINS.csv", delimiter=",",skip_header=1)  # OG PROFILE NUMBER, SAROAD, WEIGHT FRACTION
### Get list of all unique compounds.
unique_bins    = list(dict.fromkeys(bin_data[:,0]))
####################################################################################################

subPUCs = ('AS_Adhesives_Sealants','COAT_Aerosol','COAT_Allied','COAT_Architectural', \
          'CP_Detergents_Soaps','CP_General_Cleaners','FL_Fuels_Lighter','MISC_All','OG_Oil_Gas', \
          'PCP_Daily_Use_Products','PCP_Short_Use_Products','PEST_Agricultural','PEST_FIFRA')

for loopsubPUCs in subPUCs:

    ####################################################################################################
    ### Import sub-PUC data. 
    composite_data =  np.genfromtxt('./input.v1.1/'+loopsubPUCs+'.csv', delimiter=",",skip_header=1)  # Profile, %
    ####################################################################################################

    speciated_percent = composite_data[~np.isnan(composite_data[:,0])]
    total             = np.sum(speciated_percent[:,1])
    unspeciated       = 1.0 - total

    ####################################################################################################
    ### Loop to collect all profiles in sub-PUC composite and weight by % TOG emissions.
    for i in range(len(composite_data)):
        if i == 0:
            temp_array = composite_profile(composite_data[i,0],composite_data[i,1])
        else:
            temp_array = np.concatenate((temp_array[:],composite_profile(composite_data[i,0],composite_data[i,1])))
    ####################################################################################################

    ####################################################################################################
    ### Get list of all unique compounds.
    unique_compounds  = list(dict.fromkeys(temp_array[:,0]))
    ####################################################################################################

    ####################################################################################################
    ### Initialize the composite array.
    composite_array      = np.zeros((len(unique_compounds),2))
    composite_array[:,0] = unique_compounds[:]
    ####################################################################################################

    for i in range(len(composite_array)):
        all_compounds  = temp_array[temp_array[:,0]==composite_array[i,0]]
        composite_array[i,1] = np.sum(all_compounds[:,1])

    composite_array = np.concatenate((composite_array[:],np.array([[99999,unspeciated]])),axis=0)
    index           = np.argsort(-composite_array[:,1])
    composite_array = composite_array[index,:]

    ####################################################################################################
    ### Replace all Product Bins with SpecDB.xlsx specified components.
    ### AC/Consumer Product Bins are SAROAD: 44001 - 44024; Mineral Spirits/Naphtha are others.
    for i in range(len(composite_array)):
        replaced = 0
        for j in range(len(unique_bins)):
            if int(composite_array[i,0]) == unique_bins[j] and i == 0:
                bin_profile = bin_data[bin_data[:,0]==unique_bins[j]]
                bin_profile = bin_profile[:,1:]
                bin_profile[:,1] = bin_profile[:,1] * composite_array[i,1]
                final_arch_array = bin_profile[:]
                replaced = 1
                break
            elif int(composite_array[i,0]) == unique_bins[j]:
                bin_profile = bin_data[bin_data[:,0]==unique_bins[j]]
                bin_profile = bin_profile[:,1:]
                bin_profile[:,1] = bin_profile[:,1] * composite_array[i,1]
                final_arch_array = np.vstack((final_arch_array[:],bin_profile[:]))
                replaced = 1
                break
            else: pass
        if replaced == 0 and i == 0:
            final_arch_array = composite_array[i,:]
        elif replaced == 0:
            final_arch_array = np.vstack((final_arch_array[:],composite_array[i,:]))
        else: pass
    ####################################################################################################

    ####################################################################################################
    ### Get list of all unique compounds.
    unique_compounds  = list(dict.fromkeys(final_arch_array[:,0]))
    ####################################################################################################

    ####################################################################################################
    ### Initialize the final array.
    final_array      = np.zeros((len(unique_compounds),2))
    final_array[:,0] = unique_compounds[:]
    ####################################################################################################

    for i in range(len(final_array)):
        all_compounds  = final_arch_array[final_arch_array[:,0]==final_array[i,0]]
        final_array[i,1] = np.sum(all_compounds[:,1])

    index       = np.argsort(-final_array[:,1])
    final_array = final_array[index,:]
    
    ### Only report compounds > 0.01%. 
    final_array = final_array[final_array[:,1]>0.0001]
    
    ####################################################################################################
    ### Generate a per sub-PUC composite speciation file.
    headerline1   = 'SAROAD, Wt. %'
    output_file   = './output.v1.1/'+loopsubPUCs+'_TOG_profile.csv'
    np.savetxt(output_file,final_array[:],delimiter=',',header=headerline1)
    ####################################################################################################

print("Time to generate sub-PUC composites: ",datetime.now() - startTime)