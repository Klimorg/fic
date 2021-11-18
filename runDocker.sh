xhost +local:docker
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
sudo docker run \
	-it \
	--rm \
	-P \
	--privileged \
	-v $XSOCK:$XSOCK:rw \
	-v $XAUTH:$XAUTH:rw \
	-e DISPLAY=$DISPLAY \
	-e XAUTHORITY=$XAUTH \
	--network host fic:v1
xhost -local:docker

	# --device=/dev/video0:/dev/video0\