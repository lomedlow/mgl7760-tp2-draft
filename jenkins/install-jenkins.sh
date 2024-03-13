# Aller à http://localhost:8080 pour compléter l'installation

# Installer les Plugins suivants :
# - Warnings
# - XUnit
# - JDepend
# - Plot
# - Clover
# - HTML Publisher
# - Blue Ocean

########################################################
# 2. INSTALLER VIA UN DOCKERFILE
########################################################

# Construire l'image à partir du Dockerfile

docker build -t jenkins-devops:lts-jdk17 .
:'
[+] Building 157.1s (11/11) FINISHED                                                                                         
 => [internal] load .dockerignore                                                                                       0.4s
 => => transferring context: 2B                                                                                         0.0s
 => [internal] load build definition from Dockerfile                                                                    0.4s
 => => transferring dockerfile: 771B                                                                                    0.1s
 => [internal] load metadata for docker.io/jenkins/jenkins:lts-jdk17                                                    0.0s
 => [1/7] FROM docker.io/jenkins/jenkins:lts-jdk17                                                                      0.6s
 => [2/7] RUN apt-get update && apt-get install -y lsb-release                                                         10.8s
 => [3/7] RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc   https://download.docker.com/linux/debian/gp  1.0s
 => [4/7] RUN echo "deb [arch=$(dpkg --print-architecture)   signed-by=/usr/share/keyrings/docker-archive-keyring.asc]  0.8s 
 => [5/7] RUN apt-get update && apt-get install -y docker-ce-cli                                                       18.3s 
 => [6/7] RUN apt-get update && apt-get install -y ant                                                                 39.3s 
 => [7/7] RUN jenkins-plugin-cli --plugins   warnings-ng:10.7.0   jdepend:1.3.1   plot:2.1.12   xunit:3.1.3   clover:  78.1s 
 => exporting to image                                                                                                  7.4s 
 => => exporting layers                                                                                                 7.3s 
 => => writing image sha256:f1179b27882893ff33643bc2fffee65bf689ba9c2b073ddac6f103c6be202d5d                            0.0s 
 => => naming to docker.io/library/jenkins-devops:lts-jdk17
'

# Exécuter l'image comme conteneur Jenkins
#docker run -d -p 49000:8080 --restart=on-failure jenkins-devops:lts-jdk17
docker run -d -p 49000:8080 --name jenkins_biblio --restart=on-failure jenkins-devops:lts-jdk17

#A executer pour copier le mot de passe generer
#docker exec jenkins_biblio cat /var/jenkins_home/secrets/initialAdminPassword
