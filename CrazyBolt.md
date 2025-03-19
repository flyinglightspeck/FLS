# FLS with Crazyflie Bolt 

## Parts
- [Crazyflie Bolt 1.1](https://www.bitcraze.io/products/crazyflie-bolt-1-1/)
- [6000KV Motors](https://www.getfpv.com/motors/micro-quad-motors/flywoo-robo-1303-motor-6000kv.html)
- [ESC](https://www.getfpv.com/dys-xsc-20a-blheli-s-esc.html)
- [Raspberry Pi CM5](https://www.raspberrypi.com/products/compute-module-5/?variant=cm5-104032)
- [Raspberry Pi Camera Module 3 Wide NoIR](https://www.pishop.us/product/raspberry-pi-camera-module-3-wide-noir/)
- [Nano Base Board (A) for Raspberry Pi Compute Module 5](https://www.waveshare.com/cm5-nano-a.htm), also on [amazon](https://a.co/d/2dPvVRj)
- [Step down DC-DC 5V 5A voltage regulator to power Raspberry Pi](https://a.co/d/0ukGvxB)
- [Micro USB Male Port](https://a.co/d/9cJU9Qm)
- [Molex connectors](https://a.co/d/1OW0Edu)
- [Lipo Battery 850mAh 80C 11.1V 3S](https://a.co/d/hYqlLo6)

You can also use CM4 instead of CM5:
- [Raspberry Pi CM4](https://a.co/d/buHcjwu)
- [Nano Base Board (A) for Raspberry Pi Compute Module 4](https://www.waveshare.com/cm4-nano-a.htm), also on [amazon](https://a.co/d/gfsPdik)



## Configure Raspberry Pi CM4
Using and configuring Raspberry Pi Compute Module requires a baseboard, here I used WaveShare Nano Base Board (A).
The instructions are the same for CM5 except noted otherwise.
Use the compatible baseboard based on the raspberry pi model. The camera interface is not cross-compatible between CM4 and CM5. 

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

### Configure LED Strip


### USB Configuration
Ensure USB is enabled by adding the following to the RPI `/boot/firmware/config.txt`:
```
dtoverlay=dwc2,dr_mode=host
```

Connect RPi to CFBolt using usb cable.
```
$ lsusb
Bus 005 Device 003: ID 0483:5740 STMicroelectronics Virtual COM Port
Bus 005 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

Create a udev rule so that the correct permissions are applied automatically every time the device is connected.
```
sudo vim /etc/udev/rules.d/99-crazyflie.rules
```
Paste the following and save:
```
SUBSYSTEM=="usb", ATTR{idVendor}=="0483", ATTR{idProduct}=="5740", MODE="0666"
```
Apply the new rules:
```
sudo udevadm control --reload-rules
sudo udevadm trigger
```
Disconnect and reconnect the device. The new permissions should now apply automatically.

To verify, after reconnecting the Crazyflie, check the permissions again:
```
ls -l /dev/bus/usb/005/003
```
It should show:
```
crw-rw-rw- 1 root root ...
```

### Offboard Controller
Install dependencies:
```
git clone https://github.com/bitcraze/crazyflie-lib-python.git
cd crazyflie-lib-python
pip install -e .
pip install pyserial
```
```
git clone https://github.com/flslab/fls-cf-offboard-controller.git
```

### Camera Configuration
```
sudo vim /boot/firmware/config.txt
```
Add the follwing line under [cm4]:
```
dtoverlay=imx708,cam0
```


### Marker Localization
Install dependencies:
```
sudo apt install -y libopencv-dev nlohmann-json3-dev libeigen3-dev libcamera-dev
```
```
git clone git@github.com:flslab/fls-marker-localization.git
```