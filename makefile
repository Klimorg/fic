.PHONY: build_docker
build_docker:
	sudo docker build --build-arg USER_UID=$$(id -u) --build-arg USER_GID=$$(id -g) --rm -f Dockerfile -t fic:v1 .


.PHONY: run_docker
run_docker:
	sh runDocker.sh