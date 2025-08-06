import serial
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import serial.tools.list_ports

# Set up serial port and arduino connection variables
SERIAL_PORT = ''
BAUD_RATE = 9600
arduino = 0

# Set up variables to record the motor states within this program
motor_is_on = False
motor_is_going_forward = True


def list_connected_serial_ports():
    '''
        Scans serial ports and then returns a list of ports and connected devices found.
    '''
    ports = serial.tools.list_ports.comports() # get a list of all of the serial ports that are open/connected to something.
    connected_ports = [] # Create a list to contain the relevant information about the connected ports.

    for port in ports: # Iterate over all connected port
        connected_ports.append(port.device) # Add the device information from each port to the list (this is all the identifiers we need)

    return connected_ports

def open_serial_port():
    '''
        Sets up an arduino using the selected serial port.
    '''
    global arduino, SERIAL_PORT
    SERIAL_PORT = serial_port_entry.get().strip() # Get the selected serial port by taking what is currently in the entry box 
    if(SERIAL_PORT == ''): # check to make sure that we actually have something entered and that we're not trying to connect to nothing
        return
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) # Connect to the arduino port with our selected BAUD_RATE of 9600
    except serial.SerialException:
        messagebox.showerror("Error", f"Could not open {SERIAL_PORT}") # Pop up an error if we cannot connect to the port properly
        exit()

def send_command(command):
    '''
        Sends the inputted command to the serial input of the arduino.
    '''
    arduino.write(command.encode())  # Send command as bytes


def toggle_motor_state():
    '''
        Switches the motor from on to off or vice-versa.
    '''
    global motor_is_on
    if motor_is_on: # If the motor is on, toggle to off
        motor_toggle_button.config(text="OFF", bg="red") # Change the button interface
        send_command('x') # Send a serial command to the arduino to stop the motor
        motor_is_on = False # Switch our program's variable so we can keep track of the toggle
    else:
        motor_toggle_button.config(text="ON", bg="green") # Change the button interface
        send_command('s') # Send a serial command to the arduino to start the motor
        motor_is_on = True # Switch our program's variable so we can keep track of the toggle

def toggle_motor_direction():
    '''
    Switches the motor direction from forward to backward or vice-versa.
    '''
    global motor_is_going_forward
    if motor_is_going_forward: # If the motor is going forward, toggle to backward
        direction_toggle_button.config(text="BACKWARD") # Change button interface
        motor_is_going_forward = False # Switch our program's variable so we can keep track of the toggle
    else: #
        direction_toggle_button.config(text="FORWARD") # Change button interface
        motor_is_going_forward = True # Switch our program's variable so we can keep track of the toggle
    send_command('d') # Send a switch direction command to the serial input of the arduino

def update_speed():
    '''
        Changes the motor speed based on the input.
    '''
    new_speed = speed_entry.get().strip() # Get the speed from the speed input field in the GUI
    converted_speed = str(int(390.625/float(new_speed))) # Convert from a speed in mm/s to a microsecond delay for our square pulse
    send_command(converted_speed) # Update the speed by sending a serial command to the arduino
    

# Basic Tkinter GUI setup
root = tk.Tk()
root.title("Arduino Serial Control")

# Set up serial port selection & connection
serial_ports = list_connected_serial_ports()
tk.Label(root, text="Connect to Device").pack()
serial_port_entry = ttk.Combobox(root, state="normal", textvariable="Select a Device", width=20, values=serial_ports)
serial_port_entry.pack()
connect_button  = tk.Button(root, text="Connect", command=open_serial_port)
connect_button.pack(pady=20)

# Set up speed update input & submission
default_speed = tk.StringVar()
default_speed.set('1')
tk.Label(root, text="Stepper Speed mm/s:").pack()
speed_entry = ttk.Combobox(root, state="normal", textvariable=default_speed, width=20)
speed_entry.pack()
update_speed_button = tk.Button(root, text="Update Speed", command=update_speed)
update_speed_button.pack(pady=20)

# Set up on/off switch
motor_toggle_button = tk.Button(root, text="OFF", bg="green", command=toggle_motor_state)
motor_toggle_button.pack(pady=20)

# Set up direction toggle
direction_toggle_button = tk.Button(root, text="FORWARD", bg="green", command=toggle_motor_direction)
direction_toggle_button.pack(pady=20)

# Open GUI page
root.mainloop()
