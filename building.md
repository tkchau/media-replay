Building on Ubuntu 16.04
For Ubuntu 16.04 users, after installing the right packages with apt Steem will build out of the box without further effort:

# Required packages
sudo apt-get install -y \
    autoconf \
    automake \
    cmake \
    g++ \
    git \
    libbz2-dev \
    libsnappy-dev \
    libssl-dev \
    libtool \
    make \
    pkg-config \
    python3 \
    python3-jinja2

# Boost packages (also required)
sudo apt-get install -y \
    libboost-chrono-dev \
    libboost-context-dev \
    libboost-coroutine-dev \
    libboost-date-time-dev \
    libboost-filesystem-dev \
    libboost-iostreams-dev \
    libboost-locale-dev \
    libboost-program-options-dev \
    libboost-serialization-dev \
    libboost-signals-dev \
    libboost-system-dev \
    libboost-test-dev \
    libboost-thread-dev

# Optional packages (not required, but will make a nicer experience)
sudo apt-get install -y \
    doxygen \
    libncurses5-dev \
    libreadline-dev \
    perl

# Clone Steem
git clone https://github.com/nnanhthu/beowulf
cd steem sudo ip route add 172.16.0.0/24 via 192.168.122.1 dev ens3
git checkout kdev
git submodule update --init --recursive

# Install
mkdir build
cd build 
cmake -DCMAKE_BUILD_TYPE=Release -DLOW_MEMORY_NODE=ON ..
make -j $(nproc) beowulfd 
make -j $(nproc) cli_wallet

# Config file
The config.ini file is used to configure the parameters of steemd:

cd programs/steemd
mkdir data
vim data/config.ini

/data/ is directory will store all database of blockchain. Example of config files (normal node and witness node) are in /doc/ folder. 

# Start syncing 
In /build/programs/steemd:

./steemd -d data

# Become a witness

* Require: Change name and private key of your witness account in config file

- Start node
- Use client wallet with private key of account to broadcast your intent to become a witness
- Get votes
