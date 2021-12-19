#!/usr/bin/env python3

def count_increases(depths):
	increases = 0
	last_depths = depths[0:3]
	old_sum = sum(last_depths)

	for depth in depths[3:]:
		last_depths.pop(0)
		last_depths.append(depth)
		new_sum = sum(last_depths)
		if old_sum < new_sum:
			increases += 1
		old_sum = new_sum

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
