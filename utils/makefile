-include .creds

BASEIMAGE := dragonflyscience/wesm-surfaces
IMAGE := $(BASEIMAGE):2023-04-22

RUN ?= docker run --rm --net=host --user=$$(id -u):$$(id -g) -e DISPLAY=$$DISPLAY --env-file .creds -e RUN= -v$$(pwd):/work -w /work $(IMAGE)

naip-grid:
	$(RUN) python3 gridding/grid-clip-naip.py data/satellite/naip-3310

make-grid:
	$(RUN) python3 gridding/create-grid.py "EPSG:3310"

list-index:
	$(RUN) python3 process/list-index.py tahoe-2018-10n

index-workunit:
	$(RUN) python3 index/index-laz.py data/laz/tahoe-2018-10n

workunit:
	$(RUN) bash process/multi-core-laz.sh tahoe-2018-10n 

local-test: Dockerfile
	docker run -it --rm --net=host --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE) \
	bash

docker-local: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE)

docker: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE) && \
	docker push $(IMAGE) && \
	touch .push

docker-pull:
	docker pull $(IMAGE)