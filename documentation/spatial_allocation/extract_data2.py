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

years2loop      = ('02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18')

yearcounter     = 0

final_county_array        = np.zeros((len(county_fips),len(years2loop)+2))
final_county_array[:,0:2] = county_fips[:,:]
final_state_array         = np.zeros((len(state_fips),len(years2loop)+2))
final_state_array[:,0:2]  = state_fips[:,:]

for loopyears in years2loop:
    ### Import County-level data
    emp_index  = np.genfromtxt('./raw/cbp'+loopyears+'co.txt', delimiter='"',skip_header=1,dtype='str',usecols=(5))
    emp_fips   = np.genfromtxt('./raw/cbp'+loopyears+'co.txt', delimiter='"',skip_header=1,usecols=(1,3))
    if loopyears=='02' or loopyears=='03' or loopyears=='04' or loopyears=='05' or loopyears=='06' or loopyears=='18':
        emp_data   = np.genfromtxt('./raw/cbp'+loopyears+'co.txt', delimiter=",",skip_header=1,usecols=(4))
    else:
        emp_data   = np.genfromtxt('./raw/cbp'+loopyears+'co.txt', delimiter=",",skip_header=1,usecols=(5))
    if loopyears=='18':  # 2018 doesn't have employment flags
        emp_flag   = np.genfromtxt('./raw/cbp'+loopyears+'co.txt', delimiter=",",skip_header=1,dtype='str',usecols=(0))
    else:
        emp_flag   = np.genfromtxt('./raw/cbp'+loopyears+'co.txt', delimiter=",",skip_header=1,dtype='str',usecols=(3))
    if loopyears=='02':
        emp_fips   = emp_fips[emp_index[:]=='233//']
        emp_data   = emp_data[emp_index[:]=='233//']
        emp_flag   = emp_flag[emp_index[:]=='233//']
    else:
        emp_fips   = emp_fips[emp_index[:]=='236///']
        emp_data   = emp_data[emp_index[:]=='236///']
        emp_flag   = emp_flag[emp_index[:]=='236///']
    ####################################################################################################

    for i in range(len(final_county_array)):
        for j in range(len(emp_fips)):
            if final_county_array[i,0] == emp_fips[j,0] and final_county_array[i,1] == emp_fips[j,1]:
                if emp_flag[j]=='"A"':
                    final_county_array[i,2+yearcounter] = 10.
                    break
                elif emp_flag[j]=='"B"':
                    final_county_array[i,2+yearcounter] = 60.
                    break
                elif emp_flag[j]=='"C"':
                    final_county_array[i,2+yearcounter] = 175.
                    break
                elif emp_flag[j]=='"E"':
                    final_county_array[i,2+yearcounter] = 375.
                    break
                elif emp_flag[j]=='"F"':
                    final_county_array[i,2+yearcounter] = 750.
                    break
                elif emp_flag[j]=='"G"':
                    final_county_array[i,2+yearcounter] = 1750.
                    break
                elif emp_flag[j]=='"H"':
                    final_county_array[i,2+yearcounter] = 3750.
                    break
                elif emp_flag[j]=='"I"':
                    final_county_array[i,2+yearcounter] = 7500.
                    break
                elif emp_flag[j]=='"J"':
                    final_county_array[i,2+yearcounter] = 17500.
                    break
                elif emp_flag[j]=='"K"':
                    final_county_array[i,2+yearcounter] = 37500.
                    break
                elif emp_flag[j]=='"L"':
                    final_county_array[i,2+yearcounter] = 75000.
                    break
                elif emp_flag[j]=='"M"':
                    final_county_array[i,2+yearcounter] = 100000.
                    break
                else:
                    final_county_array[i,2+yearcounter] = emp_data[j]
                    break
            else: pass

    for i in range(len(final_state_array)):
        for j in range(len(final_county_array)):
            if final_state_array[i,0] == final_county_array[j,0]:
               final_state_array[i,2+yearcounter] += final_county_array[j,2+yearcounter]
            else: pass
   
    yearcounter += 1

####################################################################################################
### 
headerline1   = 'fipstate,fipscty,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018'
output_file   = './county_employment_COAT_Allied.csv'
np.savetxt(output_file,final_county_array[:],delimiter=',',header=headerline1)
####################################################################################################

####################################################################################################
### 
headerline1   = 'fipstate,fipscty,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018'
output_file   = './state_employment_COAT_Allied.csv'
np.savetxt(output_file,final_state_array[:],delimiter=',',header=headerline1)
####################################################################################################

print("Time to generate files: ",datetime.now() - startTime)