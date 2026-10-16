FROM tiryoh/ros2-desktop-vnc:humble

USER root

RUN apt-get update -q && \
    apt-get install -y --no-install-recommends \
      ros-humble-gazebo-ros-pkgs \
      ros-humble-xacro \
      python3-pytest \
      python3-matplotlib \
      ros-humble-rqt-graph \
      ros-humble-rqt-plot && \
    rm -rf /var/lib/apt/lists/*

COPY scripts/entrypoint-dev.sh /usr/local/bin/entrypoint-dev.sh
RUN chmod +x /usr/local/bin/entrypoint-dev.sh

WORKDIR /home/ubuntu/workspace

ENTRYPOINT ["/usr/local/bin/entrypoint-dev.sh"]
CMD []
