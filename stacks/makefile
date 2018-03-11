VENV_DIR ?= venv
BUILD_DIR ?= build
ENV ?= Int
STACK_NAME ?= $(shell jq ".${ENV}" stack_names.json | tr -d '"')

all: clean write-template

clean:
	rm -fr $(BUILD_DIR)

write-template: pep8
	. $(VENV_DIR)/bin/activate && python src/template.py ${ENV} > $(BUILD_DIR)/$(STACK_NAME).json

pep8: venv create-build-dir
	. $(VENV_DIR)/bin/activate && pep8 src/template.py

venv:
	test -d $(VENV_DIR) || virtualenv $(VENV_DIR)
	$(info virtualenv provisioned, please run "source $(VENV_DIR)/bin/activate if you wish to use in current shell")
	cat requirements.txt | xargs -L 1 $(VENV_DIR)/bin/pip install

create-build-dir:
	mkdir -p $(BUILD_DIR)

clean-venv:
	rm -fr $(VENV_DIR)

apply-stacks:
	./apply-stacks.sh -e $(ENV)

upload-to-s3:
	./upload-to-s3.sh