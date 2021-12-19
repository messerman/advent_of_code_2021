#!/usr/bin/env python3

def count_increases(depths):
	last_depth = 0
	increases = -1

	for depth in depths:
		if depth > last_depth:
			increases += 1
		last_depth = depth

	return increases

if '__main__' == __name__:
	done = False
	depths = []
	while not done:
		try:
			depths.append(int(input()))
			#print(depths)
		except:
			done = True

	print(count_increases(depths))
