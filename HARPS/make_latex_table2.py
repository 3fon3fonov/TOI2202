import fileinput
import os, sys
import math
import commands
import linecache
#import RV_program as RV
from numpy import *
from pylab import *
from array import *
import numpy as np
import random





##############################################################################################################################	

skip_header = 0
skip_footer = 0
format_im   = 'pdf'

jitter = 0
#mass_star = 1
offset = 0
linear_drift = 0


directory  = './'
#Kep_file  = 'J11417+427.avc.vels'
#Dyn_file  = 'RV_dyn.out' 
#Dyn_file_mod  = 'RV_dyn_mod.out'

#/home/trifonov/Archiv/GJ15AB/trifon_june/datafiles/GJ15A_harps_av-serval.vels
#/home/trifonov/Archiv/GJ15AB/trifon_june/datafiles/GJ15B_CARM-avc_avr.vels
#/home/trifonov/Archiv/GJ15AB/trifon_june/datafiles/GJ15B_harps-serval.vels
#/home/trifonov/Archiv/GJ15AB/trifon_june/datafiles/GJ15_CARM-avc_avr.vels

org_file =  'TIC358107516.drs.dat'
#org_file =  'J11417+427.avc.NIR.vels'

star = 'TIC358107516'
output_vels = 'table_%s'%star
#output_halpha = 'hlapha_%s'%star
##############################################################################################################################	



JD         = genfromtxt("%s/%s"%(directory,org_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [0])
rv        = genfromtxt("%s/%s"%(directory,org_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
sigma      = genfromtxt("%s/%s"%(directory,org_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])

bis_file = "TIC358107516_BIS_drs.dat"
bis         = genfromtxt("%s/%s"%(directory,bis_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
e_bis       = genfromtxt("%s/%s"%(directory,bis_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])

cont_file = "TIC358107516_contrast_drs.dat"
cont         = genfromtxt("%s/%s"%(directory,cont_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
e_cont       = genfromtxt("%s/%s"%(directory,cont_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])


FWHM_file = "TIC358107516_FWHM_drs.dat"
FWHM         = genfromtxt("%s/%s"%(directory,FWHM_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
e_FWHM       = genfromtxt("%s/%s"%(directory,FWHM_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])


crx_file = "TIC358107516.crx.dat"
crx         = genfromtxt("%s/%s"%(directory,crx_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
e_crx       = genfromtxt("%s/%s"%(directory,crx_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])


dlw_file = "TIC358107516.dlw.dat"
dlw         = genfromtxt("%s/%s"%(directory,dlw_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
e_dlw       = genfromtxt("%s/%s"%(directory,dlw_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])


halpha_file = "TIC358107516.halpha.dat"
halpha         = genfromtxt("%s/%s"%(directory,halpha_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
e_halpha       = genfromtxt("%s/%s"%(directory,halpha_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])

nad_I_file = "TIC358107516.nad_I.dat"
nad_I         = genfromtxt("%s/%s"%(directory,nad_I_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
e_nad_I       = genfromtxt("%s/%s"%(directory,nad_I_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])

nad_II_file = "TIC358107516.nad_II.dat"
nad_II         = genfromtxt("%s/%s"%(directory,nad_II_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [1])
e_nad_II       = genfromtxt("%s/%s"%(directory,nad_II_file),skip_header=skip_header, unpack=True,skip_footer=skip_footer, usecols = [2])



sort = sorted(range(len(JD)), key=lambda k: JD[k])


JD     = JD[sort]  
rv     = rv[sort]
sigma  = sigma[sort]

bis    = bis[sort]
e_bis  = e_bis[sort]

cont   = cont[sort]
e_cont = e_cont[sort]

FWHM   = FWHM[sort]
e_FWHM = e_FWHM[sort]

 

f = open(output_vels, 'wb') 

 
f.write("""

\\begin{table*}
\caption{HARPS Doppler measurements of %s  } 
\label{table:%s} 

\centering  

\\begin{tabular}{c c c c c c c c c c c c c c c c c c c} 

\hline\hline    
\\noalign{\\vskip 0.5mm}

Epoch [JD] & RV [m\,s$^{-1}$] & $\sigma_{RV}$ [m\,s$^{-1}$]  &  BIS [m\,s$^{-1}$] & $\sigma_{BIS}$ [m\,s$^{-1}$]  
& Contrast & $\sigma_{Contrast}$  & FWHM [m\,s$^{-1}$] & $\sigma_{FWHM}$ [m\,s$^{-1}$] &
CRX [m\,s$^{-1}$] & $\sigma_{CRX}$ &
dLW [m\,s$^{-1}$] & $\sigma_{dLW}$  &
H$_{\\alpha}$ [m\,s$^{-1}$] & $\sigma_{H$_{\\alpha}$}$  &
NaD I [m\,s$^{-1}$] & $\sigma_{NaD I}$ &
NaD II [m\,s$^{-1}$] & $\sigma_{NaD II}$   \\\  \n
\hline     
\\noalign{\\vskip 0.5mm}    

"""%(star,star))


#inst = ["HIRES","HARPS-pre","HARPS-post","CARMENES"]
#rvoff = [-0.238, -0.049,-6.177,-0.182]
#rvoff = [0.433074894160683,-0.43690837330418675,-4.66951982332346,-0.41091856169284746]
for x in range(len(JD)):
        #print JD[x], rvoff[inst_[x]]+rv[x], sigma[x], inst[inst_[x]]
	f.write('%.4f   &   %.2f   &    %.2f &   %.3f   &    %.3f &   %.3f   &    %.3f &   %.3f   &    %.3f &   %.3f   &    %.3f &   %.3f   &    %.3f &   %.3f   &    %.3f &   %.3f   &    %.3f &   %.3f   &    %.3f      \\\ \n'%(
JD[x], rv[x], sigma[x],bis[x], e_bis[x], cont[x], e_cont[x], FWHM[x], e_FWHM[x],
crx[x], e_crx[x], dlw[x], e_dlw[x], halpha[x], e_halpha[x], nad_I[x], e_nad_I[x], nad_II[x], e_nad_II[x]
  ) )



f.write("""  
\hline           
\end{tabular}


\end{table*}

""")



f.close()
 
 


















