# spongemock.py
# author: Noah Krim
# email: nkrim62@gmail.com

import random

def mock(text, diversity_bias=0.5, random_seed=None):
	# Error handling
	if diversity_bias < 0 or diversity_bias > 1:
		raise ValueError('diversity_bias must be between the inclusive range [0,1]')
	# Seed the random number generator
	random.seed(random_seed)
	# Mock the text
	out = ''
	last_was_upper = True
	swap_chance = 0.5
	for c in text:
		if c.isalpha():
			if random.random() < swap_chance:
				last_was_upper = not last_was_upper
				swap_chance = 0.5
			c = c.upper() if last_was_upper else c.lower()
			swap_chance += (1-swap_chance)*diversity_bias
		out += c
	return out