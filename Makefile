MAKEFLAGS += .silent

test:
	# Use Test Discovery mechanism
	python -m unittest

generate_TOC:
	generate_TOC.sh && echo "[OK]: Success generated TOC."

.PHONY: test generate_TOC
