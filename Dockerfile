FROM ubuntu:16.04 AS build


# Install tools required for building all programs
RUN apt-get update && apt-get install -y \
            sudo git wget time\
            build-essential gcc-5 g++-5 gcc-4.7 g++-4.7 m4 pkg-config python-pip python-setuptools python-dev python3-pip unzip \
            gcc-multilib g++-multilib libboost-dev libtiff5-dev libbz2-dev libmp3lame-dev libxslt1-dev libxml2-dev zlib1g-dev \
            libxml-libxml-perl libgomp1 libgmp-dev libmpfr-dev libmpc-dev libxi-dev libxmu-dev freeglut3-dev gettext libjasper-runtime libjasper-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install numpy

# Add qithread user
RUN useradd -ms /bin/bash qithread
RUN usermod -a -G sudo qithread
RUN echo "qithread ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers


# Copy everything into the container
COPY . /home/qithread/qithread-ae/
RUN chown -R qithread /home/qithread/qithread-ae/
USER qithread
WORKDIR /home/qithread/qithread-ae/

# Build all
# USER qithread
ENV XTERN_ROOT /home/qithread/qithread-ae/
ENV LD_LIBRARY_PATH /home/qithread/qithread-ae/dync_hook

RUN echo "Compiling QITHREAD library..."
RUN mkdir -p obj
WORKDIR /home/qithread/qithread-ae/obj/
RUN ../configure --prefix=$XTERN_ROOT/install && make && make install

RUN echo "Compiling ldap"
WORKDIR /home/qithread/qithread-ae/apps/ldap/
RUN ./mk

RUN echo "Compiling openmp library..."
WORKDIR /home/qithread/qithread-ae/apps/openmp/
RUN ./mk

RUN echo "Compiling aget..."
WORKDIR /home/qithread/qithread-ae/apps/aget
RUN ./mk


RUN echo "Compiling ImageMagick..."
WORKDIR /home/qithread/qithread-ae/apps/imagick
RUN ./mk


RUN echo "Compiling mongoose..."
WORKDIR /home/qithread/qithread-ae/apps/mongoose
RUN ./mk


RUN echo "Compiling npb..."
WORKDIR /home/qithread/qithread-ae/apps/npb
RUN ./mk


RUN echo "Compiling parsec..."
WORKDIR /home/qithread/qithread-ae/apps/parsec
RUN ./mk


RUN echo "Compiling pfscan..."
WORKDIR /home/qithread/qithread-ae/apps/pfscan
RUN ./mk


RUN echo "Compiling redis..."
WORKDIR /home/qithread/qithread-ae/apps/redis
RUN ./mk


RUN echo "Compiling stl..."
WORKDIR /home/qithread/qithread-ae/apps/stl
RUN ./mk


RUN echo "Compiling bdb_bench3n..."
WORKDIR /home/qithread/qithread-ae/apps/bdb_rep
RUN ./mk


RUN echo "Compiling mplayer mencoder..."
WORKDIR /home/qithread/qithread-ae/apps/mplayer
RUN ./mk


RUN echo "Compiling pbzip2..."
WORKDIR /home/qithread/qithread-ae/apps/pbzip2
RUN ./mk


RUN echo "Compiling phoenix..."
WORKDIR /home/qithread/qithread-ae/apps/phoenix
RUN ./mk


RUN echo "Compiling splash2x..."
WORKDIR /home/qithread/qithread-ae/apps/splash2x
RUN ./mk

# Build complete.
WORKDIR /home/qithread/qithread-ae/eval
ENTRYPOINT ["/bin/bash"]

