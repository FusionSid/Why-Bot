format:
	@python3 -m black ./

clean:
	@find . | grep -E '(__pycache__|\.pyc|\.pyo$|\.DS_Store|\.mypy_cache|\.vscode)' | xargs rm -rf
	@clear

run:
	@python3 src/main.py