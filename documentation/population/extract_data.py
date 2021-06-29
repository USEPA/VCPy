import numpy as np
from datetime import datetime

####################################################################################################

startTime = datetime.now()

####################################################################################################
### Import County FIPS
county_fips     =  np.genfromtxt("./county_fips.csv", delimiter=",",skip_header=1)
### Import State FIPS
state_fips      =  np.genfromtxt("./state_fips.csv", delimiter=",",skip_header=1)
### Import 2000-2009 County-level data
pop_2000_data   =  np.genfromtxt("./co-est00int-tot.csv", delimiter=",",skip_header=1,usecols=(3,4,8,9,10,11,12,13,14,15,16,17))
### Import 2010-2019 County-level data
pop_2010_data   =  np.genfromtxt("./co-est2019-alldata.csv", delimiter=",",skip_header=1,usecols=(3,4,9,10,11,12,13,14,15,16,17,18))
####################################################################################################

final_array        = np.zeros((len(county_fips),22))
final_array[:,0:2] = county_fips[:,:]

for i in range(len(final_array)):
    for j in range(len(pop_2000_data)):
        if final_array[i,0] == pop_2000_data[j,0] and final_array[i,1] == pop_2000_data[j,1]:
            final_array[i,2:12] = pop_2000_data[j,2:12]
            break
        else: pass
    for j in range(len(pop_2010_data)):
        if final_array[i,0] == pop_2010_data[j,0] and final_array[i,1] == pop_2010_data[j,1]:
            final_array[i,12:] = pop_2010_data[j,2:12]
            break
        else: pass

####################################################################################################
### 
headerline1   = 'fipstate,fipscty,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019'
output_file   = './county_population.csv'
np.savetxt(output_file,final_array[:],delimiter=',',header=headerline1)
####################################################################################################

final_array        = np.zeros((len(state_fips),22))
final_array[:,0:2] = state_fips[:,:]

for i in range(len(final_array)):
    for j in range(len(pop_2000_data)):
        if final_array[i,0] == pop_2000_data[j,0] and final_array[i,1] == pop_2000_data[j,1]:
            final_array[i,2:12] = pop_2000_data[j,2:12]
            break
        else: pass
    for j in range(len(pop_2010_data)):
        if final_array[i,0] == pop_2010_data[j,0] and final_array[i,1] == pop_2010_data[j,1]:
            final_array[i,12:] = pop_2010_data[j,2:12]
            break
        else: pass

####################################################################################################
### 
headerline1   = 'fipstate,fipscty,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019'
output_file   = './state_population.csv'
np.savetxt(output_file,final_array[:],delimiter=',',header=headerline1)
####################################################################################################

print("Time to generate files: ",datetime.now() - startTime)