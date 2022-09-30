format:
	@python3 -m black ./

clean:
	@find . | grep -E '(__pycache__|\.pyc|\.pyo$|\.DS_Store)' | xargs rm -r

run:
	@cd src; python3 main.py