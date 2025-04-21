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

### 3D Print
Print the following parts using Bambu PA6-CF filament.

| name          | qty |
|---------------|-----|
| frame_v3      | 1   |
| pi_holder_v2  | 4   |
| landing_gear  | 2   |
| cam_holder_l  | 1   |
| cam_holder_r  | 1   |
| sensor_holder | 1   |

Tips:
- Use smooth PEI / high temp plate.
- Clean the oil, fingerprints, and printing waste from the plate before printing.
- For the frame use 0.2mm strength profile, add 5mm of brim, and use concentric top and bottom surface pattern.
- For other parts use 0.16mm high quality profile, add brim if needed.
- After printing completes, wait util the plate temperature drops to around 40 degrees Celsius. Otherwise, the 
  printed part might bend permanently.


### Installation

1. Install the motors to the frame using the black M2 screws that are included in their package. You can install 
   them on either side of the frame.
2. Install the rubber grommets on the FC in a way that the taller part is on the side that the USB port is.
3. Solder the battery cable, Molex cable and the capacitor to the FC battery pads.
4. Install the FC on the frame. Note the orientation of the FC. The white arrow on the top of the FC shows the front 
   direction.

5. Solder the wires of the motors to the motor pads of the FC, the order of the wires does not matter.
6. Install Pi holders on the frame.
![image](images/frame_sensor_holder.jpeg)
![image](images/frame_fc.jpeg)
![image](images/fc_battery_wire.jpeg)


7. Install Pi CM5 on the frame, note the orientation.
![image](images/frame_pi.jpeg)

8. Solder a Molex cable, power adapter, and TX/RX cables on the NANO baseboard.
![image](images/nano.jpeg)
![image](images/nano_wiring_a.jpeg)
![image](images/nano_wiring_b.jpeg)

We used the 4-pin connector that comes with the FC as the TX/RX cable. We removed the black and green wires as we 
are not using them. This connector connects the FC TX to Pi RX (yellow) and FC RX to Pi TX (green).

9. Install the NANO board on the Pi CM5.
![image](images/frame_nano.jpeg)
10. Connect the TX/RX and power connector to the FC.
![image](images/fc_power_connector.jpeg)
![image](images/fc_pi_connector.jpeg)

11. Remove the camera sensor from the Raspberry Pi Camera board and install the camera holders to it using 4 M2x3 
    screws.
![image](images/cam_holder_front.jpeg)
![image](images/cam_holder_back.jpeg)

12. Install the camera holders on the Pi holders using 2 M1.4x4 screws.
13. Connect the camera board connector to the MIPI0 connector of the NANO board.
![image](images/frame_cam_holder.jpeg)

14. Do not install propellers until you have conducted the initial tests.
![image](images/v5_assembled.jpeg)


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
