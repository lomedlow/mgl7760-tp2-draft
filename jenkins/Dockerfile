FROM jenkins/jenkins:lts-jdk17
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli
RUN apt-get update && apt-get install -y ant
USER jenkins
RUN jenkins-plugin-cli --plugins \
  warnings-ng:10.7.0 \
  jdepend:1.3.1 \
  plot:2.1.12 \
  xunit:3.1.3 \
  clover:4.14.2.596.vb_4d6475e990b_ \
  htmlpublisher:1.32
