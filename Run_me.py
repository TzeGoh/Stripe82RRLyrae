##########################################################################################
#
# What: Run_me.py
#
# How : This is the main python file where you run the best periods functions . 
#       No downsampling for this, but it will give you best n number of periods 
# 
# Date : Mar 14, 2016
##########################################################################################

from gatspy import periodic

# This Function returns will give you a light curve with the n best periods
import Give_me_n_best_periods_Function as Give_Func
print("The file runs")

# This is my fitting parameters :
nterms_base=2
nterms_band=1

# This is it, this is your LombScargle code ! Pick one of the 2 below
model = periodic.LombScargleMultiband(Nterms_base=nterms_base, Nterms_band=nterms_band)
##model = periodic.SuperSmoother(fit_period=True)

# The list of light curves 
list_of_index = [82,173]
##list_of_index = [101,26,11,334,33,289,14,59,82,173]

# How many n best periods do you want from the fit?
n = 6

# Let's run it !
def main():
	for i in list_of_index:
	# It returns this : No. of observations, 'n' number of periods, and the system's best ave
		l_curves = Give_Func.give_me_n_best_periods(i,model,n)
		print(l_curves)
		print('The main loop works')
    	
main()