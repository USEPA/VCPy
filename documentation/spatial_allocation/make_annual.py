import numpy as np
from datetime import datetime

####################################################################################################

startTime = datetime.now()

####################################################################################################
### Import County FIPS
county_fips     =  np.genfromtxt("./county_fips.csv", delimiter=",",skip_header=1)
### Import State FIPS
state_fips      =  np.genfromtxt("./state_fips.csv", delimiter=",",skip_header=1)
####################################################################################################

years2loop      = ('2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018')

yearcounter     = 0

for loopyears in years2loop:
    
    final_county_array        = np.zeros((len(county_fips),len(years2loop)+2))
    final_county_array[:,0:2] = county_fips[:,:]
    final_state_array         = np.zeros((len(state_fips),len(years2loop)+2))
    final_state_array[:,0:2]  = state_fips[:,:]

    final_county_array[:,2]  = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,3]  = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,4]  = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,5]  = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,6]  = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,7]  = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,8]  = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,9]  = np.genfromtxt('./processed/county_employment_COAT_Allied.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,10] = np.genfromtxt('./processed/county_employment_COAT_Industrial.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,11] = np.genfromtxt('./processed/county_employment_PI_Printing_Inks.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,12] = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,13] = np.genfromtxt('./processed/county_pesticide_use.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,14] = np.genfromtxt('./processed/county_employment_DC_Dry_Cleaning.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,15] = np.genfromtxt('./processed/county_oilgas_well_count.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,16] = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_county_array[:,17] = np.genfromtxt('./county_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    
    final_state_array[:,2]   = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,3]   = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,4]   = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,5]   = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,6]   = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,7]   = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,8]   = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,9]   = np.genfromtxt('./processed/state_employment_COAT_Allied.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,10]  = np.genfromtxt('./processed/state_employment_COAT_Industrial.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,11]  = np.genfromtxt('./processed/state_employment_PI_Printing_Inks.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,12]  = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,13]  = np.genfromtxt('./processed/state_pesticide_use.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,14]  = np.genfromtxt('./processed/state_employment_DC_Dry_Cleaning.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,15]  = np.genfromtxt('./processed/state_oilgas_well_count.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,16]  = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))
    final_state_array[:,17]  = np.genfromtxt('./state_population.csv',delimiter=',',skip_header=1,usecols=(2+yearcounter))

    ####################################################################################################
    ### 
    headerline1   = 'fipstate,fipscty,CP_Detergents_Soaps,CP_General_Cleaners,PCP_Daily_Use_Products,PCP_Single_Use_Products,AS_Adhesives_Sealants,COAT_Architectural,COAT_Aerosol,COAT_Allied,COAT_Industrial,PI_Printing_Inks,PEST_FIFRA,PEST_Agricultural,DC_Dry_Cleaning,OG_Oil_Gas,Misc_All,FL_Fuels_Lighter'
    output_file   = './final/subpuc_county_allocation_'+loopyears+'.csv'
    np.savetxt(output_file,final_county_array[:],delimiter=',',header=headerline1)
    ####################################################################################################
    
    ####################################################################################################
    ### 
    headerline1   = 'fipstate,fipscty,CP_Detergents_Soaps,CP_General_Cleaners,PCP_Daily_Use_Products,PCP_Single_Use_Products,AS_Adhesives_Sealants,COAT_Architectural,COAT_Aerosol,COAT_Allied,COAT_Industrial,PI_Printing_Inks,PEST_FIFRA,PEST_Agricultural,DC_Dry_Cleaning,OG_Oil_Gas,Misc_All,FL_Fuels_Lighter'
    output_file   = './final/subpuc_state_allocation_'+loopyears+'.csv'
    np.savetxt(output_file,final_state_array[:],delimiter=',',header=headerline1)
    ####################################################################################################

    yearcounter += 1

print("Time to generate files: ",datetime.now() - startTime)