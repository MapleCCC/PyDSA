MAKEFLAGS += .silent

test:
	# Use Test Discovery mechanism
	python -m unittest
