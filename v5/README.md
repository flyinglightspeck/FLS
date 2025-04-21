# FLS with MicoAir H743 AIO 

## Parts
- [MicoAir H743 AIO](https://store.micoair.com/product/micoair743v2-aio-45a/)
- [6000KV Motors](https://flywoo.net/products/robo-1303-6000kv-2-4s-fpv-motor?srsltid=AfmBOooB2tLsMgUGBJvwiC2U68SPmQVYsO690a0YA3RrtI_vRBE50otv)
- [Raspberry Pi CM5](https://www.raspberrypi.com/products/compute-module-5/?variant=cm5-104032)
- [Raspberry Pi Camera Module 3 Wide NoIR](https://www.pishop.us/product/raspberry-pi-camera-module-3-wide-noir/)
- [Nano Base Board (A) for Raspberry Pi Compute Module 5](https://www.waveshare.com/cm5-nano-a.htm), also on [Amazon](https://a.co/d/2dPvVRj)
- [Pololu 5V, 5A Step-Down Voltage Regulator D24V50F5 to power Raspberry Pi](https://www.pololu.com/product/2851)
- [Molex connectors](https://a.co/d/1OW0Edu)
- [2S 650mAh 120C Lipo Battery](https://a.co/d/c1O34hy)
- [Raspberry Pi Camera Module 3 Wide NoIR](https://www.raspberrypi.com/products/camera-module-3/?variant=camera-module-3-noir-wide)
- [Raspberry Pi Camera Module 3 Sensor Cable Extension](https://www.arducam.com/200mm-sensor-extension-cable-for-raspberry-pi-v2-v3-support-working-on-raspberry-pi-and-jetson.html)
- [MicoAir MTF-02 Flow and Range Sensor](https://robofusion.net/products/micoair-optical-flow-lidar-sensor-mtf-02-compatible-with-ardupilot-px4-inav?variant=47335540359487)
- 2-inch Propellers (Any of the bellow options):
  - [Gemfan D51 Ducted 4-Blade](https://www.getfpv.com/gemfan-d51-ducted-durable-4-blade-51mm-cinewhoop-propeller-set-of-8.html?vid=13662&utm_source=google&utm_medium=cpc&utm_campaign=DM+-+NB+-+PMax+-+Shop+-+No-index+-+SM+-+ALL+%7C+Full+Funnel&utm_content=pmax_x&utm_keyword=&utm_matchtype=&campaign_id=20799936859&network=x&device=c&gc_id=20799936859&gad_source=1&gclid=Cj0KCQjwzYLABhD4ARIsALySuCQUIDG2VWcM8jVkIEcAe1tfF0vmCpzYmgZQzs1EyRDmPbsOM4Vi9hsaAoAYEALw_wcB)
  - [Gemfan Hurricane 2023S 3-Blade](https://www.getfpv.com/propellers/micro-quad-propellers/gemfan-hurricane-2023s-3-blade-propeller-set-of-8.html)
  - [HQProp T2X2X3 3-Blade](https://www.getfpv.com/propellers/micro-quad-propellers/hqprop-t2x2x3-3-blade-propeller-set-of-4.html) 

You can also use CM4 instead of CM5 (CM4 is slower than CM5):
- [Raspberry Pi CM4](https://www.raspberrypi.com/products/compute-module-4/?variant=raspberry-pi-cm4104032)
- [Nano Base Board (A) for Raspberry Pi Compute Module 4](https://www.waveshare.com/cm4-nano-a.htm), also on [Amazon](https://a.co/d/gfsPdik)


## Assembly



## Configure Raspberry Pi CM4/CM5
Using and configuring Raspberry Pi Compute Module requires a baseboard, here I used WaveShare Nano Base Board (A).
The instructions are the same for CM5 except noted otherwise.
Use the compatible baseboard based on the raspberry pi model as its camera interface is not cross-compatible between 
CM4 and CM5. 


### Install OS
Install Raspberry Pi OS 64-bit following [this guide](https://www.raspberrypi.com/documentation/computers/compute-module.html#flash-compute-module-emmc).
Configure SSH and WiFi when writing the OS using Raspberry Pi Imager.
After installing the OS, ssh to the RPi and update the packages:
```
sudo apt update && sudo apt upgrade -y
```


### Create Python Environment
```
python3 -m venv env
```

To proceed with installing Python packages activate the env:
```
source env/bin/activate
```


### Install Mavlink-Router
Install [mavlink-router](https://github.com/mavlink-router/mavlink-router?tab=readme-ov-file).

We will use this to connect to the drone using QGroundStation over WiFi and through Pi.
Replace `192.168.8.197` with the IP address of your ground computer.

```mavlink-routerd -e 192.168.8.197:14550 /dev/ttyAMA0:57600```


### Configure LED Strip
```
pip install rpi_ws281x adafruit-circuitpython-neopixel
pip install --force-reinstall adafruit-blinka
```


### Offboard Controller
TBD
```
git clone https://github.com/flslab/*.git
```


### Camera Configuration
```
sudo vim /boot/firmware/config.txt
```
Add the following line under [cm4] or [cm5]:
```
dtoverlay=imx708,cam0
```


### Marker Localization
Install dependencies:
```
sudo apt install -y cmake libopencv-dev nlohmann-json3-dev libeigen3-dev libcamera-dev
```
```
git clone https://github.com/flslab/fls-marker-localization.git
```

Build:
```
cd fls-marker-localization
mkdir build
cd build
cmake ..
make -j4
```

Copy Config:
```
cp ../src/camera_config.json .
```

Run for 10 seconds to test:
```
./eye -t 10
```
