.PHONY: data lint requirements environment

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Set up python interpreter environment and install Python dependencies
environment:
	python3 -m venv venv
	@echo ">>> New virtual environment created using python3 venv module. Activating environment."
	@bash -c "source venv/bin/activate"
	python3 -m pip install -r requirements.txt
	pip install -r requirements.txt
	cd ..

reports:
	python3 -m project/pipeline/__main__.py
