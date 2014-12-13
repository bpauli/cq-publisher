# AEM/CQ-Publisher Docker-Container

This Docker image installs [Adobe Experience Manager (formerly known as Adobe / Day CQ) ](http://docs.adobe.com/docs/en/aem/6-0.html) in Version 5.5 or later, and allows it
to be run within a Docker container. This Docker image is highly inspired by [ggotti/aem-publisher](https://github.com/ggotti/aem-publisher)

## HOW-To build your own Container

> *You must have a copy of the CQ/AEM installation Media and a valid license file

1. Copy cq-publish-4503.jar and license.properties to the current directory
2. Create a local Dockerfile and insert the following content:
```
# DOCKER-VERSION 1.0.0
FROM bpauli/cq-publisher
MAINTAINER <your_username>
```
3. Then execute your build:
```bash
docker build --tag="<your_build_tag>" .
```
4. Run your image with:
```bash
$ docker run -p 4503:4503 -d "<your_build_tag>"
```
5. Validate your running instance with:
```bash
$ docker ps -l
```

### Have fun!
