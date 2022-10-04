format:
	@python3 -m black ./

clean:
	@find . | grep -E '(__pycache__|\.pyc|\.pyo$|\.DS_Store|\.mypy_cache|\.vscode)' | xargs rm -r > /dev/null
	@clear

run:
	@cd src; python3 main.py