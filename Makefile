venv:
	@python3 -m venv venv

source:
	@source ./venv/bin/activate

format:
	@black ./

clean:
	@find . | grep -E '(__pycache__|\.pyc|\.pyo$|\.DS_Store)' | xargs rm -rf

requirements:
	@pip install -r requirements.txt

run:
	cd src; #do stuff