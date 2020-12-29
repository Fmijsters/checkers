global TURN
TURN = -1
from matplotlib import pyplot as plt
import random
import math
import decimal

def generate_grid(size):
	return [
	[0,1,0,1,0,1,0,1],
	[1,0,1,0,1,0,1,0],
	[0,1,0,1,0,1,0,1],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[-1,0,-1,0,-1,0,-1,0],
	[0,-1,0,-1,0,-1,0,-1],
	[-1,0,-1,0,-1,0,-1,0]]

	# return [
	# [0, 0,0, 0,0, 0,0,0],
	# [0, 0,0, 0,0, 0,0,0],
	# [0, 0,0, 0,0, 0,0,0],
	# [0, 0,0, 0,0, 0,0,0],
	# [0, 0,0, 0,0,-1,0,0],
	# [0, 0,-1, 0,0, 0,0,0],
	# [0, 0,0, 0,0,-1,0,0],
	# [0, 0,0, 0,0, 0,0,0]]
	# return [
	# [0, 0,0, 0,0, 0,0,0],
	# [0, 0,0, 0,0, 0,0,0],
	# [0, 0,0, 0,0, 0,0,0],
	# [0, 0,0, 0,2, 0,0,0],
	# [0, -1,0,0,0,-1,0,0],
	# [0, 0,0, 0,0, 0,0,0],
	# [0, 0,0, 0,0,-1,0,0],
	# [0, 0,0, 0,0, 0,0,0]]

def check_for_possible_king(grid):
	global TURN
	for i in range(len(grid[0])):
		if grid[0][i] == -1:
			grid[0][i] *= 2
		if grid[-1][i] == 1:
			grid[-1][i] *= 2
	return grid


def show_grid(grid,graphics=False):
	if not graphics:
		for row in grid:
			print(row)
	else:
		plt.imshow(grid, interpolation='nearest')
		plt.show()

def can_capture(grid,loc,path,final_path,cmap):
	global TURN
	could_capture = False
	inner_paths = []
	for ver in [1,-1]:
		for hor in [1,-1]:
			if 0 <= loc[1]+hor < len(grid[0]) and 0 <= loc[0]+ver < len(grid) and  0 <= loc[1]+hor*2 < len(grid[0]) and 0 <= loc[0]+ver*2 < len(grid):
				if (grid[loc[0]+ver][loc[1]+hor] == -TURN or grid[loc[0]+ver][loc[1]+hor] == -TURN*2)  and grid[loc[0]+ver*2][loc[1]+hor*2] == 0 and [loc[0]+ver*2,loc[1]+hor*2] not in path:
					could_capture = True
					inner_paths.append([loc[0]+ver*2,loc[1]+hor*2])

	if len(inner_paths) > 0:
		for p in inner_paths:
			path.append(p)
			can_capture(grid,p,path,final_path,cmap)
		final_path.append(inner_paths)
	cmap[(loc[0],loc[1])] = inner_paths
	return could_capture

def can_capture_king(grid,loc,path,final_path,cmap,taken_stones):
	global TURN
	could_capture = False
	inner_paths = []

	for i in range(1,len(grid)):
		for ver in [1,-1]:
			ver = ver*i
			for hor in [1,-1]:
				hor = hor*i
				if 0 <= loc[1]+hor < len(grid[0]) and 0 <= loc[0]+ver < len(grid) and 0 <= loc[1]+hor+round(hor/i) < len(grid[0]) and 0 <= loc[0]+ver+ round(ver/i) < len(grid):
					enemy_stone = grid[loc[0]+ver][loc[1]+hor]
					destination = grid[loc[0]+ver + round(ver/i)][loc[1]+hor+round(hor/i)]
					if (enemy_stone == -TURN or enemy_stone == -TURN *2) and destination == 0:
						if [loc[0]+ver + round(ver/i),loc[1]+hor+round(hor/i)] not in path and [loc[0]+ver,loc[1]+hor] not in taken_stones:
							could_capture = True
							inner_paths.append([loc[0]+ver+round(ver/i),loc[1]+hor + round(hor/i)])
							taken_stones.append([loc[0]+ver,loc[1]+hor])
	if len(inner_paths) > 0:
		for p in inner_paths:
			path.append(p)
			can_capture_king(grid,p,path,final_path,cmap,taken_stones)
		final_path.append(inner_paths)
	cmap[(loc[0],loc[1])] = inner_paths
	return could_capture
	
def paths(d, _start, _current = []):
  if _current:
    yield _current
  for i in d[(_start[0],_start[1])]:
     if i not in _current:
        yield from paths(d, i, _current+[i])

def get_move_for_stone(grid,r,c):
	global TURN
	moves = []
	capture_dict ={}
	n_capture_dict= {}
	captures = []
	if can_capture(grid,[r,c],[],[],capture_dict):
		rev_keys = list(capture_dict.keys())
		rev_keys.reverse()
		for k in rev_keys:
			n_capture_dict[k] = capture_dict[k]
		results = [c for i in n_capture_dict for c in paths(n_capture_dict, i, [i])]
		_max_len = max(map(len, results))
		_paths = [i for i in results if len(i) == _max_len]
		for _path in _paths:
			captures = _path
	else:
		for hor in [1,-1]:
			if 0 <= c+hor < len(grid[0]) and 0 <= r+TURN < len(grid):
				# empty square
				if grid[r+TURN][c+hor] == 0:
					moves.append([r+TURN,c+hor])
				# ally square
				elif grid[r+TURN][c+hor] == TURN:
					pass

	return moves,captures

def get_move_for_king(grid,r,c):
	global TURN
	moves = []
	capture_dict ={}
	n_capture_dict= {}
	captures = []
	if can_capture_king(grid,[r,c],[],[],capture_dict,[]):
		rev_keys = list(capture_dict.keys())
		rev_keys.reverse()
		for k in rev_keys:
			n_capture_dict[k] = capture_dict[k]
		results = [c for i in n_capture_dict for c in paths(n_capture_dict, i, [i])]
		_max_len = max(map(len, results))
		_paths = [i for i in results if len(i) == _max_len]
		for _path in _paths:
			captures = _path
	else:
		for i in range(len(grid)):
			#				 DR     UR     DL      UL
			for ver,hor in [[1,1],[-1,1],[1,-1],[-1,-1]]:
				new_r = r+ (ver*i)
				new_c = c+ (hor*i)
				if 0 > new_c or new_c >= len(grid[0]) or len(grid) <= new_r or new_r < 0:
					continue
				if (grid[new_r][new_c] >= TURN and TURN > 0) or (grid[new_r][new_c] <= TURN and TURN < 0):
					continue
				moves.append([new_r,new_c])
	return moves,captures

def get_all_moves(grid):
	global TURN
	all_moves= {}
	all_captures = {}
	for r in range(len(grid)):
		for c in range(len(grid[r])):
			if grid[r][c] == TURN*2:
				moves,captures = get_move_for_king(grid,r,c)
				if len(moves) > 0:
					all_moves[(r,c)] = moves
				if len(captures) > 0:
					all_captures[(r,c)] = captures
			if grid[r][c] == TURN:
				moves,captures = get_move_for_stone(grid,r,c)
				if len(moves) > 0:
					all_moves[(r,c)] = moves
				if len(captures) > 0:
					all_captures[(r,c)] = captures
	if len(all_captures)>0:
		return all_captures,True
	else:
		return all_moves,False

def pick_random_move(moves,is_capture):
	if not is_capture:
		random_key = random.sample(moves.keys(),1)[0]
		random_move = None
		if len(moves[random_key]) > 1:
			random_move = random.sample(moves[random_key],1)
		else:
			random_move = moves[random_key]

		return random_key,random_move
	else:
		random_key = random.sample(moves.keys(),1)[0]
		random_move = moves[random_key]
		return random_key,random_move

def do_move(grid,stone,destination,visualize):
	global TURN
	if len(destination) == 1:
		destination = destination[0]
	grid[destination[0]][destination[1]] = grid[stone[0]][stone[1]]
	grid[stone[0]][stone[1]] = 0
	grid = check_for_possible_king(grid)
	if visualize:
		show_grid(grid,graphics=True)
	return grid

def make_capture(grid,stone,destination,visualize):
	middle_stone = [round((stone[0]+destination[0])/2),round((stone[1]+destination[1])/2)]
	if grid[stone[0]][stone[1]] == TURN * 2:
		x1,y1 = stone
		x2,y2 = destination
		#rechts onder
		if x2>x1 and y2>y1:
			middle_stone = [destination[0]-1,destination[1]-1]
	    #links onder
		if x2<x1 and y2>y1:
			middle_stone = [destination[0]+1,destination[1]-1]
		#rechts boven
		if x2>x1 and y2<y1:
			middle_stone = [destination[0]-1,destination[1]+1]
		#links boven
		if x2<x1 and y2<y1:
			middle_stone = [destination[0]+1,destination[1]+1]
	grid[middle_stone[0]][middle_stone[1]] = 0
	grid = do_move(grid,stone,destination,visualize)
	return grid,destination

def do_capture(grid,stone,destination,visualize):
	del destination[0]
	for des in destination:
		grid,stone = make_capture(grid,stone,des,visualize)
	return grid

def play_rounds(n_rounds,grid,visualize=False):
	global TURN
	for i in range(n_rounds):
		moves,is_capture = get_all_moves(grid)
		if len(moves) == 0:
			return grid
		stone,destination = pick_random_move(moves,is_capture)
		if not is_capture:
			grid = do_move(grid,stone,destination,visualize)
		else:
			grid = do_capture(grid,stone,destination,visualize)
		TURN *=-1
		# print(i)
	return grid

def calculate_winner(grid):
	decimal.getcontext().rounding = decimal.ROUND_HALF_UP
	winner = 0
	draw =False
	for r in grid:
		for c in r:
			if c == 0:
				continue
			if winner != 0 and (c != winner and c != round(winner*2) and round(c/2)!=winner):
				draw = True
			if winner == 0:
				winner = decimal.Decimal(c/2).to_integral_value()
	if draw or winner ==0:
		return 0
	return winner



def main():
	pos = 0
	neg = 0
	draw = 0
	for i in range(1000):
		# show_grid(grid,graphics=True)
		grid = generate_grid(10)
		grid= play_rounds(1000,grid,visualize=False)
		winner = calculate_winner(grid)
		if winner>0:
			pos += 1
		elif winner == 0:
			draw += 1
		else:
			neg += 1
	print('1:',pos,'draw:',draw,'-1:',neg)
	# show_grid(grid,graphics=True)

if __name__=='__main__':
	main()