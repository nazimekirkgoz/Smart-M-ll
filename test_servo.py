import machine
import time

# Pin definition
SERVO_PIN = 13
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50)

def set_servo_angle(angle):
    # Mapping 0-180 to ~26-128 duty
    duty = int(((angle / 180) * (128 - 26)) + 26)
    servo.duty(duty)
    print(f"Angle: {angle}, Duty: {duty}")
    time.sleep(0.5) # Give it time to move
    servo.duty(0)   # Stop signal to prevent jitter
    print("Servo Signal Off")

print("--- Servo Test Start (Pulse & Release) ---")
print("If motor buzzes but doesn't move, unplug immediately.")

try:
    # Test 1: Move to center (90)
    print("Moving to 90 (Center)...")
    set_servo_angle(90)
    time.sleep(1)

    # Test 2: Gentle movements
    print("Moving to 20 (Soft Closed)...")
    set_servo_angle(20) 
    time.sleep(1)

    print("Moving to 90...")
    set_servo_angle(90)
    time.sleep(1)
    
except Exception as e:
    print(f"Error: {e}")

finally:
    servo.deinit()
    print("Servo Released")
