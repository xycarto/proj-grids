
BASEIMAGE := xycarto/proj-grids
IMAGE := $(BASEIMAGE):2023-04-22

RUN ?= docker run -it --rm --net=host \
	--user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	-e RUN= \
	-v$$(pwd):/work \
	-w /work \
	$(IMAGE)

# Run like: make build-grid epsg="EPSG:3310" width=100 height=100
build-grid:
	$(RUN) python3 create-grid.py $(epsg) $(width) $(height)

local-test: Dockerfile
	docker run -it --rm --net=host --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE) \
	bash

docker-local: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE)

docker: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE) && \
	docker push $(IMAGE)

docker-pull:
	docker pull $(IMAGE)