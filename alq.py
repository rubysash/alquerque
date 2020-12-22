import pygame	# the main workhorse
import os		# i KNOW I'll need to detect OS and handle paths, etc
import sys		# for sys.exit
import math 	# for square roots on hex and other polygons

# allows us to use the == QUIT later instead of pygame.locals.QUIT
from pygame.locals import * 

WH = (255,255,255)	# white
BL = (0,0,0)		# black
GY = (128,128,128)	# grey
RE = (255,0,0)		# red

# this can be adjusted if you like
scale = 55  # 30-80 is probably best scale range
num_sq = 8	# must be multiple of 2


# offset is designed to match board specifically, don't change
offset = 1.5
start = offset
step = int(8/num_sq)  # how big should each square be?
end = 8/step		# should just be the same as squares
steps = int(num_sq / 2)
stepsq = offset

# relative game board size
W  = int(step * scale * num_sq + 3*scale)
H  = int(step * scale * num_sq + 3*scale)
 
# basic grid layout for all squares
coors = []
start0 = []
start2 = []
for click in range(0,num_sq+1,1):
	coors.append(start)
	start = start + step

# Generic counter, it's irrelevant, but makes unique dict keys
counter = 100

# Lets make some dots
dots = {}
for x in coors:
	for y in coors:
		dots[counter] = [x,y]
		counter += 1 # gets everything except outer edge.

# and our squares dict
squares = {}
for x in coors[:-1]:
	for y in coors[:-1]:
		squares[counter] = [x,y,scale,scale]
		counter += 1 # gets everything except outer edge.

# finally the lines dict
lines = {}
for n in range(0,steps,1):
	start0.append(stepsq)
	stepsq = stepsq + 2 * step

# What is a better way to write this?
# have to jump the lines around then loop over this
stepsq = 2 * step + offset
for n in range(0,steps,1):
	start2.append(stepsq)
	stepsq = stepsq + 2 * step

# My x and y arrays are built for / lines
# loop over each and draw the lines
# double duty and populate %dots too please
for y1 in start0:
	for x1 in start0:
		x2 = x1 + 2 * step
		y2 = y1 + 2 * step
		lines[counter] = [x1,y1,x2,y2]
		counter += 1

# now loop over the \ lines 
for y1 in start0:
	for x1 in start2:
		x2 = x1 - 2 * step
		y2 = y1 + 2 * step
		lines[counter] = [x1,y1,x2,y2]
		counter += 1

def main():
	# can't run pygame without init, just do it
	pygame.init()

	# clock required to limit fps
	FPS = pygame.time.Clock()

	# one of (possibly many) surfaces to draw on
	SURF = pygame.display.set_mode((W,H))

	# the title bar
	pygame.display.set_caption("Alquerque Board")

	# default colors start at black
	r1,g1,b1 = (0,0,0)
	r2,g2,b2 = (0,0,0)

	# default x and y, until you click
	lw = 3            # line width of polygons

	# used to pulse color
	flip_r1,flip_g1,flip_b1 = (1,1,1)
	flip_r2,flip_g2,flip_b2 = (1,1,1)

	#Game loop begins
	while True:
		# current color of pulse, r,g,b set at bottom of while 
		r1,flip_r1 = get_pulse(flip_r1,r1,1) # mix and match your pulse, red
		b2,flip_b2 = get_pulse(flip_b2,b2,5) # mix and match your pulse, red
		pulse1 = (r1,g1,b1)
		pulse2 = (r2,g2,b2)

		# fill our surface with white
		SURF.fill(GY)

		# event section
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:

				# update where we just clicked
				(x,y) = pygame.mouse.get_pos()

			if event.type == QUIT:
				# pygame has a buggy quit, do both
				pygame.quit()
				sys.exit()

		draw_board(SURF,pulse1,pulse2,lw)
		# update the screen object itself
		pygame.display.update()	# update entire screen if no surface passed

		# tick the fps clock
		FPS.tick(60)

'''
moved out to clean up the main()
'''
def draw_board(surf,pulse1,pulse2,lw):

	for s in squares:
		pygame.draw.rect(surf, pulse1,
			[
				int(squares[s][0]*scale),
				int(squares[s][1]*scale),
				int(step*scale),
				int(step*scale)
			],
			lw
		)

	for xy in lines:
		pass
		pygame.draw.line(surf,pulse1,
			(lines[xy][0] * scale,lines[xy][1] * scale),
			(lines[xy][2] * scale,lines[xy][3] * scale),
			lw
		)

	# placing dots last so they look like they are "on top"
	for xy in dots:
		pygame.draw.circle(surf, pulse2, (
				dots[xy][0] * scale, 
				dots[xy][1] * scale
				), 
			lw*2, 0
		)

'''
just pulse 255 to 0 back to 255 repeat 
set boundaries so we don't get invalid rgb value
input: state of the flip, and current color code
return: updated flip and color code
'''
def get_pulse(flipped,c,step):

	if flipped:
		if c < 255: c += step
		else:
			c = 255
			flipped = 0
	else:
		if c > step: c -= step
		else:
			c = 0
			flipped = 1

	if c > 255: c = 255
	if c < 0: c = 0

	return (c,flipped)



if __name__ == '__main__':
	# capture ctrl c
	try:
		main()
	except KeyboardInterrupt:
		# pygame has a buggy quit, do both
		pygame.quit()
		sys.exit()



