import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import random
from math import ceil
from matplotlib.patches import Rectangle
from z3 import *


parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument("--instances_path", help="Path where the instances are stored", required = True, type=str)
parser.add_argument("--file_name", help="Name of the file", required = True, type=str)
args = parser.parse_args()

def main():
	
	if not os.path.exists(args.instances_path[:-9] + 'SMT/out'):
		os.makedirs(args.instances_path + 'SMT/out')
		
	file = open(args.instances_path + '/' + args.file_name,"r") 
	
	# Create the output file
	file_out = open(args.instances_path[:-9] + 'SMT/out/'+ args.file_name[:-4] + "-out_general.txt", "w+") 

	# Read the first line which contains the width of the PCB
	first_line = file.readline()
	width = int(first_line)

	# Read the second line which contains the number of chips
	second_line = file.readline()
	number_of_chips = int(second_line)
	
	# Read all the remaining lines which contains the horizontal and vertical dimensionof the i-th piece of the chip
	remaining_lines = file.readlines()
	
	# To remove empty lines
	remaining_lines = [line.strip() for line in remaining_lines if line.strip()]
	
	couples = {}
	chips = []
	area = 0
	x,y = 0,1

	
	i = 0
	for line in remaining_lines:
		couple = line.replace(" ", "").strip()
		size = line.split(" ")
		area += int(size[0])*int(size[1])
		if size[0] != size[1]:
			chips.append([[int(size[0]),int(size[1])], [int(size[1]),int(size[0])]])
		else:
			chips.append([[int(size[0]),int(size[1])], [-1,-1]])
		i+=1
		couples[couple] = couples.get(couple,0) + 1
		
	ncopy = list(couples.values())
	number_of_different_chips = np.array([ncopy]).size
	min_height  = ceil(area/width)
	print("Number of chips: ", chips, "Height: ", min_height,"Width: ",  width,"Number of chips", number_of_chips, "Area is: ", area)

	
	# Variables
	O = [ [ Int("o_{}_{}".format(i+1, j+1)) for j in range(2) ]for i in range(number_of_chips) ]
	P = [ [ Int("p_{}_{}".format(i+1, j+1)) for j in range(2) ]for i in range(number_of_chips) ]
	max_height = 0
	for i in range(len(chips)):
		print("CHIPS")
		print(chips[i], chips[i][0][1])
		max_height+= chips[i][0][1]
	print('max_height', max_height)
	# Constraints
	
	rotation = [Or(And(P[i][x] == chips[i][0][x], P[i][y] == chips[i][0][y]), And(P[i][x] == chips[i][1][x], P[i][y] == chips[i][1][y], P[i][x] != -1) ) for i in range(number_of_chips)]

	for height in range(min_height, max_height):
		in_domain = [ And(O[i][x] >= 0, O[i][x] < width, O[i][y] >= 0, O[i][y] < height) for i in range(number_of_chips)] 
		print('********************* ')
		print("Rotation obtained: ", rotation)
		print("in domain obtained are: ", in_domain)
		
		# chips fit in the board
		in_board = [ And(P[i][x] + O[i][x] <= width, P[i][y] + O[i][y] <= height ) for i in range(number_of_chips)] 
			
		# non-overlapping
		no_overlap = []		
		for i in range(number_of_chips):
			for j in range(number_of_chips):
				if (i<j):
					no_overlap.append(Or(O[i][x]+ P[i][x]  <= O[j][x], O[j][x]+ P[j][x]<= O[i][x], O[i][y]+ P[i][y]  <= O[j][y], O[j][y] + P[j][y] <= O[i][y]))
					
		
		implied = []
		for i in range(width):
			for j in range(number_of_chips):
				implied.append(Sum([If(And(O[j][x] <= i, i < O[j][x] + P[j][x]), P[j][y],0) for j in range(number_of_chips)]) <= height)
		
		for i in range(height):
			for j in range(number_of_chips):
				implied.append(Sum([If(And( O[j][y] <= i, i < O[j][y] + P[j][y]), P[j][x],0) for j in range(number_of_chips)]) <= width)
		base = []
		for i in range(number_of_different_chips):
			if i == 0:
				base.append(0)
			else:
				base.append(sum(ncopy[0:i]))
								
		order = []
		for i in range(number_of_different_chips):
			for j in range(ncopy[i]-1):
				order.append(And(O[base[i]+j][x] >= O[base[i]+j+1][x], Implies(O[base[i]+j][x] == O[base[i]+j+1][x],O[base[i]+j][y] >= O[base[i]+j+1][y])))
		
					
		constraints = in_domain + rotation + in_board + no_overlap + order 
		
		# Create the solver
		s = Solver()
		s.add(constraints)
		fig = plt.figure(figsize=(5 + (width//8) ,5 + (height//8)))
		ax = fig.gca(title = "Plot of the solution")
			
		
		if s.check() == sat:
		
			m = s.model()
			
			print("{} {}".format(width, height))
			file_out.write("{} {}\n".format(width, height))
			
			print("{}".format(number_of_chips))
			file_out.write("{}\n".format(number_of_chips))

			for i in range(number_of_chips):
				print("{:<1} {:<3} {:<1} {:<2}".format(str(m[P[i][x]]),str(m[P[i][y]]), str(m[O[i][x]]), str(m[O[i][y]])))
				file_out.write("{:<1} {:<3} {:<1} {:<2}\n".format(str(m[P[i][x]]), str(m[P[i][y]]), str(m[O[i][x]]), str(m[O[i][y]])))
				color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
				sq = Rectangle(( m[O[i][x]].as_long(),  m[O[i][y]].as_long()),m[P[i][x]].as_long(),m[P[i][y]].as_long(),fill = True,color=color[0], alpha=.3 )
				ax.add_patch(sq)
					
			print("\n{}\n".format(s.statistics()))
			plt.plot()
			plt.show()
			break
		else: 
			print("Failed to solve with height: ", height)
	
	file.close() 
	file_out.close()
		
if __name__ == "__main__":
	main()