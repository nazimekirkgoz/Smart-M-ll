# pyrefly: ignore [missing-import]
import machine, time

class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor measures the distance from an object in front of it.
    """
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readout pin to measure pulse width
        echo_timeout_us: Timeout in microseconds (default for ~5m)
        """
        self.echo_timeout_us = echo_timeout_us
        self.trig = machine.Pin(trigger_pin, mode=machine.Pin.OUT, pull=None)
        self.trig.value(0)
        self.echo = machine.Pin(echo_pin, mode=machine.Pin.IN, pull=None)

    def _send_pulse_and_return_time(self):
        """
        Sends a 10us pulse and waits for the echo.
        Returns the pulse duration in microseconds.
        """
        self.trig.value(0)
        time.sleep_us(5)
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        # Wait for echo to start
        pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
        return pulse_time

    def distance_cm(self):
        """
        Get the distance in centimeters.
        """
        pulse_time = self._send_pulse_and_return_time()
        if pulse_time <= 0:
            return -1 # Timeout or error
        
        # Speed of sound is 340 m/s or 0.034 cm/us. 
        # Distance = time * speed / 2 (round trip)
        distance = (pulse_time * 0.03432) / 2
        return distance

    def distance_mm(self):
        """
        Get the distance in millimeters.
        """
        return self.distance_cm() * 10
