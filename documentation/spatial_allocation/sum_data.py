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

naics2loop      = ('COAT_Industrial','PI_Printing_Inks')

for loopnaics in naics2loop:

    final_county_array        = np.zeros((len(county_fips),len(years2loop)+2))
    final_county_array[:,0:2] = county_fips[:,:]
    final_state_array         = np.zeros((len(state_fips),len(years2loop)+2))
    final_state_array[:,0:2]  = state_fips[:,:]

    ### Import County-level data
    if loopnaics == 'COAT_Industrial':
       county_emp_a   = np.genfromtxt('processed/county_employment_'+loopnaics+'_a.csv',delimiter=',',skip_header=1)
       county_emp_b   = np.genfromtxt('processed/county_employment_'+loopnaics+'_b.csv',delimiter=',',skip_header=1)
       county_emp_c   = np.genfromtxt('processed/county_employment_'+loopnaics+'_c.csv',delimiter=',',skip_header=1)
       county_emp_d   = np.genfromtxt('processed/county_employment_'+loopnaics+'_d.csv',delimiter=',',skip_header=1)
       county_emp_e   = np.genfromtxt('processed/county_employment_'+loopnaics+'_e.csv',delimiter=',',skip_header=1)
       county_emp_f   = np.genfromtxt('processed/county_employment_'+loopnaics+'_f.csv',delimiter=',',skip_header=1)
       county_emp_g   = np.genfromtxt('processed/county_employment_'+loopnaics+'_g.csv',delimiter=',',skip_header=1)
       county_emp_h   = np.genfromtxt('processed/county_employment_'+loopnaics+'_h.csv',delimiter=',',skip_header=1)
       county_emp_i   = np.genfromtxt('processed/county_employment_'+loopnaics+'_i.csv',delimiter=',',skip_header=1)
       county_emp_j   = np.genfromtxt('processed/county_employment_'+loopnaics+'_j.csv',delimiter=',',skip_header=1)
       county_emp_k   = np.genfromtxt('processed/county_employment_'+loopnaics+'_k.csv',delimiter=',',skip_header=1)
       county_emp_l   = np.genfromtxt('processed/county_employment_'+loopnaics+'_l.csv',delimiter=',',skip_header=1)
       county_emp_m   = np.genfromtxt('processed/county_employment_'+loopnaics+'_m.csv',delimiter=',',skip_header=1)
       county_emp_n   = np.genfromtxt('processed/county_employment_'+loopnaics+'_n.csv',delimiter=',',skip_header=1)
       county_emp_o   = np.genfromtxt('processed/county_employment_'+loopnaics+'_o.csv',delimiter=',',skip_header=1)
       county_emp_p   = np.genfromtxt('processed/county_employment_'+loopnaics+'_p.csv',delimiter=',',skip_header=1)
       county_emp_q   = np.genfromtxt('processed/county_employment_'+loopnaics+'_q.csv',delimiter=',',skip_header=1)
       county_emp_r   = np.genfromtxt('processed/county_employment_'+loopnaics+'_r.csv',delimiter=',',skip_header=1)
       county_emp_s   = np.genfromtxt('processed/county_employment_'+loopnaics+'_s.csv',delimiter=',',skip_header=1)
       county_emp_t   = np.genfromtxt('processed/county_employment_'+loopnaics+'_t.csv',delimiter=',',skip_header=1)
       county_emp_u   = np.genfromtxt('processed/county_employment_'+loopnaics+'_u.csv',delimiter=',',skip_header=1)
       county_emp_v   = np.genfromtxt('processed/county_employment_'+loopnaics+'_v.csv',delimiter=',',skip_header=1)
       county_emp_w   = np.genfromtxt('processed/county_employment_'+loopnaics+'_w.csv',delimiter=',',skip_header=1)
       county_emp_x   = np.genfromtxt('processed/county_employment_'+loopnaics+'_x.csv',delimiter=',',skip_header=1)
       county_emp_y   = np.genfromtxt('processed/county_employment_'+loopnaics+'_y.csv',delimiter=',',skip_header=1)
       county_emp_z   = np.genfromtxt('processed/county_employment_'+loopnaics+'_z.csv',delimiter=',',skip_header=1)
       county_emp_aa  = np.genfromtxt('processed/county_employment_'+loopnaics+'_aa.csv',delimiter=',',skip_header=1)
       county_emp_ab  = np.genfromtxt('processed/county_employment_'+loopnaics+'_ab.csv',delimiter=',',skip_header=1)
       county_emp_ac  = np.genfromtxt('processed/county_employment_'+loopnaics+'_ac.csv',delimiter=',',skip_header=1)
       county_emp_ad  = np.genfromtxt('processed/county_employment_'+loopnaics+'_ad.csv',delimiter=',',skip_header=1)
       county_emp_ae  = np.genfromtxt('processed/county_employment_'+loopnaics+'_ae.csv',delimiter=',',skip_header=1)
       county_emp_af  = np.genfromtxt('processed/county_employment_'+loopnaics+'_af.csv',delimiter=',',skip_header=1)
       county_emp_ag  = np.genfromtxt('processed/county_employment_'+loopnaics+'_ag.csv',delimiter=',',skip_header=1)
       county_emp_ah  = np.genfromtxt('processed/county_employment_'+loopnaics+'_ah.csv',delimiter=',',skip_header=1)

    elif loopnaics == 'PI_Printing_Inks':
       county_emp_a   = np.genfromtxt('processed/county_employment_'+loopnaics+'_a.csv',delimiter=',',skip_header=1)
       county_emp_b   = np.genfromtxt('processed/county_employment_'+loopnaics+'_b.csv',delimiter=',',skip_header=1)

    else: print('there is an issue with your NAICS')

    ### Import State-level data
    if loopnaics == 'COAT_Industrial':
       state_emp_a   = np.genfromtxt('processed/state_employment_'+loopnaics+'_a.csv',delimiter=',',skip_header=1)
       state_emp_b   = np.genfromtxt('processed/state_employment_'+loopnaics+'_b.csv',delimiter=',',skip_header=1)
       state_emp_c   = np.genfromtxt('processed/state_employment_'+loopnaics+'_c.csv',delimiter=',',skip_header=1)
       state_emp_d   = np.genfromtxt('processed/state_employment_'+loopnaics+'_d.csv',delimiter=',',skip_header=1)
       state_emp_e   = np.genfromtxt('processed/state_employment_'+loopnaics+'_e.csv',delimiter=',',skip_header=1)
       state_emp_f   = np.genfromtxt('processed/state_employment_'+loopnaics+'_f.csv',delimiter=',',skip_header=1)
       state_emp_g   = np.genfromtxt('processed/state_employment_'+loopnaics+'_g.csv',delimiter=',',skip_header=1)
       state_emp_h   = np.genfromtxt('processed/state_employment_'+loopnaics+'_h.csv',delimiter=',',skip_header=1)
       state_emp_i   = np.genfromtxt('processed/state_employment_'+loopnaics+'_i.csv',delimiter=',',skip_header=1)
       state_emp_j   = np.genfromtxt('processed/state_employment_'+loopnaics+'_j.csv',delimiter=',',skip_header=1)
       state_emp_k   = np.genfromtxt('processed/state_employment_'+loopnaics+'_k.csv',delimiter=',',skip_header=1)
       state_emp_l   = np.genfromtxt('processed/state_employment_'+loopnaics+'_l.csv',delimiter=',',skip_header=1)
       state_emp_m   = np.genfromtxt('processed/state_employment_'+loopnaics+'_m.csv',delimiter=',',skip_header=1)
       state_emp_n   = np.genfromtxt('processed/state_employment_'+loopnaics+'_n.csv',delimiter=',',skip_header=1)
       state_emp_o   = np.genfromtxt('processed/state_employment_'+loopnaics+'_o.csv',delimiter=',',skip_header=1)
       state_emp_p   = np.genfromtxt('processed/state_employment_'+loopnaics+'_p.csv',delimiter=',',skip_header=1)
       state_emp_q   = np.genfromtxt('processed/state_employment_'+loopnaics+'_q.csv',delimiter=',',skip_header=1)
       state_emp_r   = np.genfromtxt('processed/state_employment_'+loopnaics+'_r.csv',delimiter=',',skip_header=1)
       state_emp_s   = np.genfromtxt('processed/state_employment_'+loopnaics+'_s.csv',delimiter=',',skip_header=1)
       state_emp_t   = np.genfromtxt('processed/state_employment_'+loopnaics+'_t.csv',delimiter=',',skip_header=1)
       state_emp_u   = np.genfromtxt('processed/state_employment_'+loopnaics+'_u.csv',delimiter=',',skip_header=1)
       state_emp_v   = np.genfromtxt('processed/state_employment_'+loopnaics+'_v.csv',delimiter=',',skip_header=1)
       state_emp_w   = np.genfromtxt('processed/state_employment_'+loopnaics+'_w.csv',delimiter=',',skip_header=1)
       state_emp_x   = np.genfromtxt('processed/state_employment_'+loopnaics+'_x.csv',delimiter=',',skip_header=1)
       state_emp_y   = np.genfromtxt('processed/state_employment_'+loopnaics+'_y.csv',delimiter=',',skip_header=1)
       state_emp_z   = np.genfromtxt('processed/state_employment_'+loopnaics+'_z.csv',delimiter=',',skip_header=1)
       state_emp_aa  = np.genfromtxt('processed/state_employment_'+loopnaics+'_aa.csv',delimiter=',',skip_header=1)
       state_emp_ab  = np.genfromtxt('processed/state_employment_'+loopnaics+'_ab.csv',delimiter=',',skip_header=1)
       state_emp_ac  = np.genfromtxt('processed/state_employment_'+loopnaics+'_ac.csv',delimiter=',',skip_header=1)
       state_emp_ad  = np.genfromtxt('processed/state_employment_'+loopnaics+'_ad.csv',delimiter=',',skip_header=1)
       state_emp_ae  = np.genfromtxt('processed/state_employment_'+loopnaics+'_ae.csv',delimiter=',',skip_header=1)
       state_emp_af  = np.genfromtxt('processed/state_employment_'+loopnaics+'_af.csv',delimiter=',',skip_header=1)
       state_emp_ag  = np.genfromtxt('processed/state_employment_'+loopnaics+'_ag.csv',delimiter=',',skip_header=1)
       state_emp_ah  = np.genfromtxt('processed/state_employment_'+loopnaics+'_ah.csv',delimiter=',',skip_header=1)

    elif loopnaics == 'PI_Printing_Inks':
       state_emp_a   = np.genfromtxt('processed/state_employment_'+loopnaics+'_a.csv',delimiter=',',skip_header=1)
       state_emp_b   = np.genfromtxt('processed/state_employment_'+loopnaics+'_b.csv',delimiter=',',skip_header=1)

    else: print('there is an issue with your NAICS')

    ####################################################################################################

    if loopnaics == 'COAT_Industrial':
       final_county_array[:,2:] = county_emp_a[:,2:] + county_emp_b[:,2:] + county_emp_c[:,2:] + county_emp_d[:,2:] + county_emp_e[:,2:] + county_emp_f[:,2:] + county_emp_g[:,2:] + county_emp_h[:,2:] + county_emp_i[:,2:] + county_emp_j[:,2:] + county_emp_k[:,2:] + county_emp_l[:,2:] + county_emp_m[:,2:] + county_emp_n[:,2:] + county_emp_o[:,2:] + county_emp_p[:,2:] + county_emp_q[:,2:] + county_emp_r[:,2:] + county_emp_s[:,2:] + county_emp_t[:,2:] + county_emp_u[:,2:] + county_emp_v[:,2:] + county_emp_w[:,2:] + county_emp_x[:,2:] + county_emp_y[:,2:] + county_emp_z[:,2:] + county_emp_aa[:,2:] + county_emp_ab[:,2:] + county_emp_ac[:,2:] + county_emp_ad[:,2:] + county_emp_ae[:,2:] + county_emp_af[:,2:] + county_emp_ag[:,2:] + county_emp_ah[:,2:]
       final_state_array[:,2:]  = state_emp_a[:,2:]  + state_emp_b[:,2:]  + state_emp_c[:,2:]  + state_emp_d[:,2:]  + state_emp_e[:,2:]  + state_emp_f[:,2:]  + state_emp_g[:,2:]  + state_emp_h[:,2:]  + state_emp_i[:,2:]  + state_emp_j[:,2:]  + state_emp_k[:,2:]  + state_emp_l[:,2:]  + state_emp_m[:,2:]  + state_emp_n[:,2:]  + state_emp_o[:,2:]  + state_emp_p[:,2:]  + state_emp_q[:,2:]  + state_emp_r[:,2:]  + state_emp_s[:,2:]  + state_emp_t[:,2:]  + state_emp_u[:,2:]  + state_emp_v[:,2:]  + state_emp_w[:,2:]  + state_emp_x[:,2:]  + state_emp_y[:,2:]  + state_emp_z[:,2:] + state_emp_aa[:,2:]  + state_emp_ab[:,2:]  + state_emp_ac[:,2:]  + state_emp_ad[:,2:]  + state_emp_ae[:,2:]  + state_emp_af[:,2:]  + state_emp_ag[:,2:]  + state_emp_ah[:,2:]
    elif loopnaics == 'PI_Printing_Inks':
       final_county_array[:,2:] = county_emp_a[:,2:] + county_emp_b[:,2:]
       final_state_array[:,2:]  = state_emp_a[:,2:]  + state_emp_b[:,2:]
    else: print('there is an issue with your NAICS')

    ####################################################################################################
    ### 
    headerline1   = 'fipstate,fipscty,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018'
    output_file   = './processed/county_employment_'+loopnaics+'.csv'
    np.savetxt(output_file,final_county_array[:],delimiter=',',header=headerline1)
    ####################################################################################################
    
    ####################################################################################################
    ### 
    headerline1   = 'fipstate,fipscty,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018'
    output_file   = './processed/state_employment_'+loopnaics+'.csv'
    np.savetxt(output_file,final_state_array[:],delimiter=',',header=headerline1)
    ####################################################################################################

print("Time to generate files: ",datetime.now() - startTime)