FROM centos:7
#Hotfixing systemctl in centos container, we should not do this as containers are not designed to have services
#The following section is from https://github.com/docker-library/docs/tree/master/centos#systemd-integration
#We begin be removing unneeded service so they dont start at spawining our init
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]
#Start instaling python environment
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y python36u python36u-libs python36u-devel python36u-pip
#Installing Flask
#I didnt use python virtual env but it shoud be used
RUN pip3.6 install Flask \
    && pip3.6 install prometheus_client
#Copy our python code & Service file
COPY ./app/msg_of_the_day.py /bin/msg_of_the_day/ \
    && msg_of_the_day.service /usr/lib/systemd/system/
#The Enable the service
RUN /bin/systemctl enable msg_of_the_day.service
#Exposing port 5000 to the host
EXPOSE 5000
#Start init which will spawn systemd services thats why we cleaned unneeded service at the beginning
CMD ["/usr/sbin/init"]
