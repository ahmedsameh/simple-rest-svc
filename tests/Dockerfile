FROM centos:7
#Start instaling python environment
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y python36u python36u-libs python36u-devel python36u-pip
#Installing Flask
#I didnt use python virtual env but it shoud be used
RUN pip3.6 install Flask
RUN pip3.6 install nose2

