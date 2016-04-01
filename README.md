###################################################################################
#
#   What : README.md
#  
#   For  : Run_me.py , Give_me_5_best_periods_Function.py
#
#   How : Stripe82RRLyrae:
#			Searching LSST-pipeline Stripe 82 photometry for RR Lyrae.
#
#	Date : Mar 14, 2016
#
###################################################################################

Stripe82RRLyrae:
	Searching LSST-pipeline Stripe 82 photometry for RR Lyrae.
	
	
Why : 
	This read_me should tell you everything about how to find best_periods  
          for RR_Lyraes	
          
Where ( in Github ) :
	From April 1st, 2016 onwards, I would be writing + changing scripts exclusively on 
		Github. It's located here : 
			/Users/Tzegoh/Documents/Stripe82RRLyrae/scripts	
				
My short-hand:
	# : This is the title
	##: You can usually uncover these for something meaningful, like a truncated list
		or a very helpful print command
		
Difference between 2 Run_Me:
	"Run_me.py" will give you the no. of obs, 5 best periods + system's
		best ave of those periods
	"Run_me_with_down_sample.py" will give you  the no. of obs, 5 best periods + system's
		best ave of those periods, but it would have down-sampled it for you

Word of caution ( if you want to run it on your computer ):
	Do not run the main file from text wrangler.
	Do run it as :
		python Run_me.py
			on Terminal, after changing directories to the location stated in 'where'