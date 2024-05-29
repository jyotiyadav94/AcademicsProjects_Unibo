import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import random
from math import ceil
from matplotlib.patches import Rectangle
from z3 import *


parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument("--instances_path",help="Path where the instances are located", required=True, type=str)
parser.add_argument("--file_name", help="Name of the file",required=True, type=str)
args = parser.parse_args()

def main():
	if not os.path.exists(args.instances_path[:-9] + 'SMT/out'):
		os.makedirs(args.instances_path + 'SMT/out')
		
	file = open(args.instances_path + '/' + args.file_name,"r")
	
	# Create the output file
	file_out = open(args.instances_path[:-9] + 'SMT/out/'+ args.file_name[:-4] + "-out_base.txt", "w+") 

	#Read first line that contains the width of board
	first_line = file.readline()
	width = int(first_line)

	# Read the second line which contains the number of chips to be placed on board
	second_line = file.readline()
	number_of_chips = int(second_line)

	# Read all the remaining lines which contains the horizontal and vertical dimensionof the i-th piece of chips
	remaining_lines = file.readlines()
	# To remove empty lines
	remaining_lines = [line.strip() for line in remaining_lines if line.strip()]

	chips = []
	area = 0
	x,y = 0,1
	for line in remaining_lines:
		line = line.split(" ")
		val = [int(line[x]),int(line[y])]
		chips.append(val)
		area += val[x]*val[y]
	min_height = ceil(area/width)
	print("Number of chips: ", chips, "Height: ", min_height,"Width: ",  width,"Number of chips", number_of_chips, "Area is: ", area)

	max_height = 0
	for i in range(len(chips)):
		max_height+= chips[i][1]
	print('max_height', max_height)

	O = [ [ Int("o_{}_{}".format(i+1, j+1)) for j in range(2) ]for i in range(number_of_chips) ]

	
	for height in range(min_height, max_height):
		in_domain = [ And(O[i][x] >= 0, O[i][x] < width, O[i][y] >= 0, O[i][y] < height) for i in range(number_of_chips)] 
			
		# chips fit in the rectangle
		in_board = [ And(chips[i][x] + O[i][x] <= width, chips[i][y] + O[i][y] <= height ) for i in range(number_of_chips)] 
		
		# non-overlapping
		no_overlap = []		
		for i in range(number_of_chips):
			for j in range(number_of_chips):
				if (i<j):
					no_overlap.append(Or(O[i][x]+ chips[i][x]  <= O[j][x], O[j][x]+ chips[j][x]<= O[i][x], O[i][y]+ chips[i][y]  <= O[j][y], O[j][y] + chips[j][y] <= O[i][y]))
					

		implied = []
		for i in range(width):
			for j in range(number_of_chips):
				implied.append(Sum([If(And(O[j][x] <= i, i < O[j][x] + chips[j][x]), chips[j][y],0) for j in range(number_of_chips)]) <= height)

		for i in range(height):
			for j in range(number_of_chips):
				implied.append(Sum([If(And( O[j][y] <= i, i < O[j][y] + chips[j][y]), chips[j][x],0) for j in range(number_of_chips)]) <= width)
				

		constraints = in_domain + in_board + no_overlap 

		# Create the solver
		s = Solver()
		s.add(constraints)
		fig = plt.figure(figsize=(5 + (width//8) ,5 + (height//8)))
		ax = fig.gca(title = "Plot of the solution")\

		if s.check() == sat:
			m = s.model()
			
			print("{} {}".format(width, height))
			file_out.write("{} {}\n".format(width, height))
			
			print("{}".format(number_of_chips))
			file_out.write("{}\n".format(number_of_chips))

			for i in range(number_of_chips):
				print("{:<1} {:<3} {:<1} {:<2}".format(chips[i][x], chips[i][y], str(m[O[i][x]]), str(m[O[i][y]])))
				file_out.write("{:<1} {:<3} {:<1} {:<2}\n".format(chips[i][x], chips[i][y], str(m[O[i][x]]), str(m[O[i][y]])))
				color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
				sq = Rectangle(( m[O[i][x]].as_long(),  m[O[i][y]].as_long()),chips[i][x],chips[i][y],fill = True,color=color[0], alpha=.3 )
				ax.add_patch(sq)
					
			print("\n{}\n".format(s.statistics()))
			
			plt.plot()
			plt.show()
			break
		else: 
			print("Failed to solve with height: ", height)
	file.close()
	file_out.close()

if __name__ == '__main__':
	main()
