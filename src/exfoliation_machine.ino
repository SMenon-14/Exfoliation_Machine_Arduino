 #include <Arduino.h>

// These are the pins we connected our driver to on our arduino (see wiring diagram)
const int DIR = 2;
const int PUL = 4;

// These booleans will hold the current status of whether or not we are running and which way we are running
bool running = false;
bool direction = true;

// This value will hold the length of our square pulse
int stepDelay = 1000;

void setup() {
  // Set up our pins as outputs
  pinMode(DIR, OUTPUT);
  pinMode(PUL, OUTPUT);

  // This will just set the initial direction to LOW
  digitalWrite(DIR, direction ? HIGH : LOW);
  /** Translation of the ternary operator
   * (condition ? output if true : output if false)
   * In other words, it's just a weird looking if-else statement, you could just write it as below:
   * 
   * if(direction){
   *    digitalWrite(DIR, HIGH);
   * } else {
   *    digitalWrite(DIR, LOW);
   * }
   * 
   * Remember that if(direction) works because direction is a bool and therefore is just true or false.
   */


  // This sets up our serial input
  Serial.begin(9600);
  //Serial.println("Enter 's' to start, 'x' to stop, 'd' to change direction"); <--- this would just prompt the user in the serial monitor (but we aren't using it)
}

void stepPulse(int delay){
  /**
 * @brief Sends a command to the arduino to have the motor move one step with the given delay
 *
 * This function takes in a delay between high and low and sends out a single square pulse with that delay for the motor to move.
 *
 * @param delay The delay between steps.
 * 
      Time --->

      HIGH  ┌──────┐      ┌──────┐      ┌──────┐
            │      │      │      │      │      │
            │      │      │      │      │      │
      LOW   └──────┘──────┘──────┘──────┘──────┘
            ^      ^      ^      ^      ^
            Rise  Fall   Rise   Fall   Rise
 */

    digitalWrite(PUL, HIGH);
    delayMicroseconds(delay);
    digitalWrite(PUL, LOW);
    delayMicroseconds(delay);
}

void loop() {
  // Check for key input
  if (Serial.available() > 0) {
    char incomingCommand = Serial.peek();  // Look at next character (without removing it from our input stream)

    // If it's a letter command ('s', 'x', or 'd')
    if (isAlpha(incomingCommand)) {
      incomingCommand = Serial.read();  // Read the char (removing it from our input stream)
      
      // Check what our case our char command corresponds to
      if (incomingCommand == 's') {
        running = true; // <--- if our incoming command is 's', we want to make sure our motor is running
        //Serial.println("Started motor"); <--- this would confirm the action was carried our in the serial monitor (use for debugging)
      } else if (incomingCommand == 'x') {
        running = false; // <--- if our incoming command is 's', we want to make sure our motor is stopped
        //Serial.println("Stopped motor"); <--- this would confirm the action was carried our in the serial monitor (use for debugging)
      } else if (incomingCommand == 'd') {
        direction = !direction; // Swap the direction
        digitalWrite(DIR, direction ? HIGH : LOW); // Send the set direction to the motor
        //Serial.println(direction ? "Direction: FORWARD" : "Direction: REVERSE"); <--- this would confirm the action was carried our in the serial monitor (use for debugging)
      }
    }
    // If it's a digit, parse it as a new step delay value
    else if (isDigit(incomingCommand)) {
      // Read out the full int value
      int newDelay = Serial.parseInt();
      // Confirm that we have a valid input value so we aren't damaging the motor at all
      if (newDelay > 300 && 3000 > newDelay) {
        stepDelay = newDelay; // Set our delay value to the new one
        //Serial.print("New delay: ");
        //Serial.println(stepDelay);
      }
    } else {
      Serial.read();  // Discard unexpected input
    }
}

  // If running, send pulses
  if (running) {
    stepPulse(stepDelay);
  }
}
