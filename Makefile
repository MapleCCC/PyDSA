MAKEFLAGS += .silent

TEST_DIR := tests
SRC_DIR := algorithms

TEST_COMMAND_INSTALLED := hash COMMAND 2>/dev/null || { echo >&2 "COMMAND is not installed. Try 'pip install COMMAND'. Aborting."; exit 1; }

test:
	# Use Test Discovery mechanism
	python -m unittest discover $(TEST_DIR)

coverage:
	$(TEST_COMMAND_INSTALLED:COMMAND=coverage)
	coverage run -m unittest discover $(TEST_DIR)
	coverage html
	python -c "import os; import webbrowser; url='file://'+os.path.join(os.getcwd(), 'htmlcov/index.html'); webbrowser.open(url)"

freeze_requirements:
	# $(TEST_COMMAND_INSTALLED:COMMAND=pipreqs)
	hash pipreqs 2>/dev/null || { pip freeze > requirements.txt; exit 1; }
	pipreqs .

generate_toc:
	generate_toc.sh && echo "[OK]: Success generated TOC."

clean:
	# git clean -fdx
	rm -rf htmlcov/ bin/

.PHONY: test coverage freeze_requirements generate_toc clean
