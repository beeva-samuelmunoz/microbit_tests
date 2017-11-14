#
# Author: Samuel M.H. <samuel.mh@gmail.com>
# Description:
#    Make-based utility to manage the project.
#    Idea taken from:
#     - http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

#
### PATHS
#
LIBRARY = 'smh_microbit'


#Don't touch
PATH_PROJECT = $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))
PATH_VENV = $(PATH_PROJECT)'/venv3.5'
PATH_LIBRARY = $(PATH_PROJECT)'/'$(LIBRARY)


#
### Autodocumenting thing, don't touch
#
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



#
### Install the project
#


install: ## Create a development environment (virtualenv).
	@echo "Create the environment in "$(PATH_PROJECT)
	@virtualenv -p python3.5 $(PATH_VENV)
	@echo "Install requirements"
	# Install packages in order
	$(PATH_VENV)'/bin/pip' install -r $(PATH_PROJECT)'/deploy/requirements.txt'
	@echo "Create symbolic links"
	# Link to project
	@ln -s $(PATH_PROJECT) $(PATH_VENV)'/'
	# Link code to project library so it is in the PYTHONPATH
	@ln -s $(PATH_LIBRARY) $(PATH_VENV)'/lib/python3.5/site-packages/'
	@echo "Done"



#
### Orientation Demo
#

orientation-flash_usb_logger: ## Flash the microbit with the USB logger.
	@echo "Flashing USB microbit logger"
	@$(PATH_VENV)/bin/uflash smh_microbit/orientation/microbit/usb_logger.py
	@echo "Restarting the board ..."
	@sleep 20
	@echo "Flashing libs"
	@$(PATH_VENV)/bin/ufs put smh_microbit/orientation/microbit/data.py


orientation-flash_radio_logger: ## Flash the microbit with the radio logger.


orientation-flash_radio_receiver: ## Flash the microbit with the radio receiver.


orientation-run_visualization: ## Run visualization example.
	@cd smh_microbit/orientation/pc;$(PATH_VENV)'/bin/python3.5' visualization.py;cd $(PATH_PROJECT)

orientation-run_webvisualization: ## Run visualization example on browser.
		@cd smh_microbit/orientation/pc;$(PATH_VENV)'/bin/python3.5' webserver.py;cd $(PATH_PROJECT)




run_game: ## Start the game
	@$(PATH_VENV)'/bin/python3.5' -m smh_eyetracking.game.game

build_features: ## Build the features02 dataset
	@$(PATH_VENV)'/bin/python3.5' -m smh_eyetracking.features02.build

build_features-augmented: ## Build the features02 dataset
	@$(PATH_VENV)'/bin/python3.5' -m smh_eyetracking.features02.build_augmented

inspect_dataset: ## Inspect the dataset
	@$(PATH_VENV)'/bin/python3.5' -m smh_eyetracking.inspect_dataset.inspect_dataset

start_notebooks: ## Start the Jupyter notebook server
	@$(PATH_VENV)/bin/jupyter notebook --NotebookApp.default_url=/tree/smh_eyetracking/notebooks --ip=0.0.0.0
