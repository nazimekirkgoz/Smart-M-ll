import machine
import time
import sys

# --- Config ---
SERVO_PIN = 13
FREQ = 50

# Setup
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=FREQ)

def set_angle(angle):
    if angle < 0: angle = 0
    if angle > 180: angle = 180
    # Map 0-180 to 26-128
    duty = int(((angle / 180) * (128 - 26)) + 26)
    try:
        servo.duty(duty)
        print(f"Angle: {angle} | Duty: {duty}")
    except Exception as e:
        print(f"Error setting duty: {e}")
    return angle

def main():
    print("--- Servo Limit Finder ---")
    print("Commands:")
    print("  +  : Increase angle by 5")
    print("  -  : Decrease angle by 5")
    print("  0  : Go to 0")
    print("  9  : Go to 90")
    print("  f  : Free/Detach servo (Stop signal)")
    print("  q  : Quit")
    
    current_angle = 90
    current_angle = set_angle(current_angle)
    
    while True:
        cmd = input("Cmd [+/-/0/9/f/q]: ").strip().lower()
        
        if cmd == 'q':
            break
        elif cmd == '+':
            current_angle += 5
            current_angle = set_angle(current_angle)
        elif cmd == '-':
            current_angle -= 5
            current_angle = set_angle(current_angle)
        elif cmd == '0':
            current_angle = 0
            current_angle = set_angle(current_angle)
        elif cmd == '9':
            current_angle = 90
            current_angle = set_angle(current_angle)
        elif cmd == 'f':
            servo.duty(0)
            print("Servo detached (signal off)")
        elif cmd == '':
            pass
        else:
            try:
                val = int(cmd)
                if 0 <= val <= 180:
                    current_angle = val
                    current_angle = set_angle(current_angle)
            except:
                print("Invalid command")
                
    print("Exiting...")
    servo.deinit()

if __name__ == '__main__':
    main()
