.PHONY: build_docker
build_docker:
	sudo docker build --build-arg USER_UID=$$(id -u) --build-arg USER_GID=$$(id -g) --rm -f Dockerfile -t fic:v1 .

# .PHONY: build_docker_dev
# build_docker-dev:
# 	sudo docker build --build-arg USER_UID=$$(id -u) --build-arg USER_GID=$$(id -g) --rm -f Dockerfile.dev -t fic:v1-dev .


.PHONY: run_docker
run_docker:
	sh runDocker.sh


.PHONY: run_docker_dev
run_docker_dev:
	sh runDocker_dev.sh
