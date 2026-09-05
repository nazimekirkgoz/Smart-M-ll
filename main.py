# pyrefly: ignore [missing-import]
import machine
import time
from hcsr04 import HCSR04

# --- Configuration ---
# Pins
TRIG_PIN = 5
ECHO_PIN = 18
SERVO_PIN = 13

# Constants
DISTANCE_THRESHOLD = 25   # Distance in cm to trigger opening
OPEN_ANGLE = 90
# Reduced from 90 to be safe
CLOSED_ANGLE = 0        # Increased from 15 to avoid mechanical stress
HOLD_TIME = 0             # Seconds to stay open after hand is gone (0 = hemen kapat)
COOLDOWN_TIME = 2         # Seconds to wait after closing before re-checking sensor
SERVO_STEP_DELAY = 0       # [SPEED CONTROL] 0 = En hızlı, 0.02+ = Yavaş/Stabil

# --- Initialization ---
sensor = HCSR04(trigger_pin=TRIG_PIN, echo_pin=ECHO_PIN)
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50)

def set_angle_duty(angle):
    """Calculates duty for a given angle and sets it."""
    # Mapping 0-180 to ~26-128 duty
    duty = int(((angle / 180) * (128 - 26)) + 26)
    servo.duty(duty)

def smooth_servo_move(start_angle, end_angle):
    """Moves the servo gradually to prevent current spikes."""
    STEP_SIZE = 5      # Derece adım boyutu — büyütünce daha hızlı
    MIN_STEP_DELAY = 0.015  # 15ms minimum — servo fiziksel olarak yetişsin
    step = STEP_SIZE if end_angle > start_angle else -STEP_SIZE
    for angle in range(start_angle, end_angle, step):
        set_angle_duty(angle)
        time.sleep(max(SERVO_STEP_DELAY, MIN_STEP_DELAY))
    
    set_angle_duty(end_angle)
    time.sleep(0.5) # Increased: servo'nun hedefe ulaşması için bekle
    servo.duty(0)   # IMPORTANT: Cut power to stop jitter/buzzing

def get_median_distance(samples=5):
    """Reads sensor multiple times and uses median to filter noise."""
    readings = []
    for _ in range(samples):
        try:
            d = sensor.distance_cm()
            if 2 < d < 400: # Valid range for HC-SR04
                readings.append(d)
        except:
            pass
        time.sleep(0.02) # Short delay between readings
    
    if not readings:
        return 999
    
    readings.sort()
    return readings[len(readings) // 2] # Return the middle value (Median)

def manage_lid():
    print("Smart Trash Can starting...")
    current_angle = CLOSED_ANGLE
    
    # Ensure lid is closed at start
    set_angle_duty(CLOSED_ANGLE)
    time.sleep(1)
    servo.duty(0) # IMPORTANT: Detach to stop buzz/jitter at start
    
    print(f"Ready. Waiting for object < {DISTANCE_THRESHOLD}cm")
    print(f"Current Speed Delay: {SERVO_STEP_DELAY}s (Change 'SERVO_STEP_DELAY' to adjust)")

    while True:
        try:
            # Using median filter for stability
            distance = get_median_distance(samples=5)
            
            if distance < DISTANCE_THRESHOLD:
                print(f"Object detected ({distance:.1f}cm)! Opening...")
                smooth_servo_move(current_angle, OPEN_ANGLE)
                current_angle = OPEN_ANGLE
                
                # --- Keep lid open while hand/object is still present ---
                # Reset hold timer each time we still see something
                hold_elapsed = 0
                CHECK_INTERVAL = 0.2  # seconds between re-checks while open
                while hold_elapsed < HOLD_TIME:
                    time.sleep(CHECK_INTERVAL)
                    hold_elapsed += CHECK_INTERVAL
                    still_there = get_median_distance(samples=3)
                    if still_there < DISTANCE_THRESHOLD:
                        # Object still detected — reset timer
                        hold_elapsed = 0
                
                print("Closing...")
                smooth_servo_move(current_angle, CLOSED_ANGLE)
                current_angle = CLOSED_ANGLE
                
                # --- Cooldown: ignore sensor for a moment after closing ---
                # Prevents the sensor (or lid itself) from immediately re-triggering
                print(f"Cooldown {COOLDOWN_TIME}s...")
                time.sleep(COOLDOWN_TIME)
                
                print("Idle...")
                
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(1)
            
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        manage_lid()
    except KeyboardInterrupt:
        print("Stopping...")
        servo.deinit()

