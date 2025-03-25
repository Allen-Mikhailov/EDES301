# Python Commands

### Pip install
```bash
sudo python3.11 -m pip install foo
```

### Install python3.11
```bash
# note it may be wise to extend space requirements 

# getting dependencies
sudo apt update && sudo apt install -y \
    build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev \
    libsqlite3-dev libbz2-dev liblzma-dev curl

sudo apt install -y libffi-dev
sudo apt install -y python3-smbus i2c-tools libgpiod2 libopenjp2-7 libtiff5 # not entirely sure these are needed

# building python (this will take hours probably)
cd /usr/src
sudo curl -O https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
sudo tar -xf Python-3.11.0.tgz
cd Python-3.11.0
sudo ./configure --enable-optimizations
sudo make -j$(nproc)
sudo make altinstall

# Installing pip
sudo curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
```

### Rebuild python
```bash
cd /usr/src/Python-3.11.0  # Go to the Python source directory
sudo make clean  # Clean previous build
sudo ./configure --enable-optimizations
sudo make -j$(nproc)  # This will take some time
sudo make altinstall
```

### Install packages
```bash
sudo python3.11 -m pip install adafruit-circuitpython-ssd1306
sudo python3.11 -m pip install adafruit-blinka
sudo python3.11 -m pip install numpy
# i think there is one more that has something to do with BBIO

# building pillow from source
# instructions from https://pillow.readthedocs.io/en/stable/installation/building-from-source.html#building-from-source

# depenencies
# if it asks you to switch out a package do it (I forgot which one)
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev 
sudo apt-get install libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk 
sudo apt-get install libharfbuzz-dev libfribidi-dev libxcb1-dev

sudo python3.11 -m pip install --upgrade Pillow --no-binary :all: --no-cache-dir

```