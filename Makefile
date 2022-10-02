format:
	@python3 -m black ./

clean:
	@find src/ | grep -E '(__pycache__|\.pyc|\.pyo$|\.DS_Store)' | xargs rm -r > /dev/null

run:
	@cd src; python3 main.py