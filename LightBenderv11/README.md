# ArduPilot Parameters
Load the ap_lightbender.params file or set the following parameters on the ArduPilot:

ARMING_CHECK 0

BATT_ARM_VOLT 7.5
BATT_CAPACITY 650
BATT_CRT_VOLT 7.2
BATT_LOW_VOLT 7.3

COMPASS_USE Disabled
COMPASS_USE2 Disabled
COMPASS_USE3 Disabled

EK3_MAG_CAL Use external yaw sensor
EK3_SRC1_POSZ GPS
EK3_SRC1_POSXY GPS
EK3_SRC1_VELZ GPS
EK3_SRC1_VELXY GPS
EK3_SRC1_YAW GPS

GPS_DELAY_MS 50
GPS_TYPE MAV

GYRO_FILTER 100

INS_LOG_BAT_MASK 1
INS_LOG_BAT_OPT 5
INS_HNTCH_ENABLE 1
INS_HNTCH_HMNCS 1 (set to 7 for three harmonics for tri-blade props)
INS_HNTCH_MODE 3 (ESC Telemetry)
INS_HNTCH_FREQ 400 (average hover RPM / 60)
INS_HNTCH_BW 100 (INS_HNTCH_FREQ / 4)
INS_HNTCH_REF 1
INS_HNTCH_OPTS 6 (Multi-source, Update at loop rate)
INS_HNTCH_FREQ 425 (average hover RPM / 60)
INS_HNTCH_BW 40 (at most INS_HNTCH_FREQ / 4)
INS_HNTCH_OPTS# ArduPilot Parameters
Load the ap_lightbender.params file or set the following parameters on the ArduPilot:

ARMING_CHECK 0

BATT_ARM_VOLT 7.5
BATT_CAPACITY 650
BATT_CRT_VOLT 7.2
BATT_LOW_VOLT 7.3

COMPASS_USE Disabled
COMPASS_USE2 Disabled
COMPASS_USE3 Disabled

EK3_MAG_CAL Use external yaw sensor
EK3_SRC1_POSZ GPS
EK3_SRC1_POSXY GPS
EK3_SRC1_VELZ GPS
EK3_SRC1_VELXY GPS
EK3_SRC1_YAW GPS

GPS_DELAY_MS 50
GPS_TYPE MAV

INS_GYRO_FILTER 162
INS_LOG_BAT_MASK 1
INS_LOG_BAT_OPT 5
INS_HNTCH_ENABLE 1
INS_HNTCH_HMNCS 1 (set to 7 for three harmonics for tri-blade props)
INS_HNTCH_MODE 3 (ESC Telemetry)
INS_HNTCH_FREQ 400 (average hover RPM / 60)
INS_HNTCH_BW 100 (INS_HNTCH_FREQ / 4)
INS_HNTCH_REF 1
INS_HNTCH_OPTS 6 (Multi-source, Update at loop rate)
INS_HNTCH_FREQ 375 (around average hover RPM / 60)
INS_HNTCH_BW 40 (start with INS_HNTCH_FREQ / 4 then narrow down)
INS_HNTCH_OPTS 6 (Multi-source, Update at loop rate)

LAND_SPEED 30

LOG_BITMASK 2504447 (Check all except for mission commands, optical flow, camera, raw imu, and video stabilization)

OSD_CELL_COUNT 2

RPM1_TYPE 5 (ESC Telemetry Motors Bitmask)

RPM1_ESC_MASK 15 (Channels 1 - 4)
SERVO_BLH_BDMASK 15 (Channels 1 - 4)
SERVO_BLH_POLES 14 (If using another motor count the number of magnets inside the rotor and put in the correct number)
SERVO_DSHOT_ESC 1 (BLHeli32/Kiss/AM32)

SERIAL1_BAUD 921600

VISO_TYPE MAVLink


LAND_SPEED 30

LOG_BITMASK 2504447 (Check all except for mission commands, optical flow, camera, raw imu, and video stabilization)

OSD_CELL_COUNT 2

RPM1_TYPE 5 (ESC Telemetry Motors Bitmask)

RPM1_ESC_MASK 15 (Channels 1 - 4)
SERVO_BLH_BDMASK 15 (Channels 1 - 4)
SERVO_BLH_POLES 14 (If using another motor count the number of magnets inside the rotor and put in the correct number)
SERVO_DSHOT_ESC 1 (BLHeli32/Kiss/AM32)

SERIAL1_BAUD 921600

VISO_TYPE MAVLink