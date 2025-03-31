REGION=us-east-1
PACKAGE_NAME=yaml_layer

.PHONY: build clean

build:
	mkdir -p python
	pip install pyyaml -t python
	zip -r ${PACKAGE_NAME}.zip python

clean:
	rm -rf python ${PACKAGE_NAME}.zip