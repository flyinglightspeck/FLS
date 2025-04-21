import serial
import struct

ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def send_msp_command(command):
    """Send an MSP command without a payload."""
    packet = b'$M<' + bytes([0, command, command])  # Checksum = XOR of payload and command
    ser.write(packet)

def read_msp_response():
    """Read MSP response dynamically."""
    header = ser.read(3)
    if header != b'$M>':
        print(f"Invalid header: {header}")
        return None

    length_byte = ser.read(1)
    if not length_byte:
        print("No length byte received.")
        return None

    length = ord(length_byte)
    command = ser.read(1)
    payload = ser.read(length)
    checksum = ser.read(1)

    print(f"Raw Response: payload={payload.hex()}")

    if len(payload) != length:
        print(f"Warning: Expected {length} bytes, received {len(payload)} bytes.")

    if len(payload) >= 2:
        distance_cm = struct.unpack('<H', payload[:2])[0] / 10.0  # Convert to cm
        print(f"Distance from floor: {distance_cm} cm")
    else:
        print("Unknown response format.")

send_msp_command(151)  # MSP_RANGEFINDER
read_msp_response()