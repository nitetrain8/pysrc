	from random import randint 
	while True:
		problem_amount = int(input("How many problems would you like to solve? ")) 
		if 0 < problem_amount < 11:
			break
		print("Sorry, that isn't a valid number.") 
