-include .creds

BASEIMAGE := xycarto/proj-grids
IMAGE := $(BASEIMAGE):2023-04-22

RUN ?= docker run --rm --net=host --user=$$(id -u):$$(id -g) -e DISPLAY=$$DISPLAY --env-file .creds -e RUN= -v$$(pwd):/work -w /work $(IMAGE)

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
	echo $(DOCKER_PW) | docker login --username xycarto --password-stdin
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE) && \
	docker push $(IMAGE)

docker-pull:
	docker pull $(IMAGE)