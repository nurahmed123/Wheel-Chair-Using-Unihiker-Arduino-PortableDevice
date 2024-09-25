// Pin definitions for L298N motor driver
const int motor1Pin1 = 2; // IN1 (Motor 1 forward)
const int motor1Pin2 = 3; // IN2 (Motor 1 backward)
const int motor2Pin1 = 4; // IN3 (Motor 2 forward)
const int motor2Pin2 = 5; // IN4 (Motor 2 backward)

void setup() {
  // Set motor pins as output
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);

  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  // Check if any data is available to read from serial port
  if (Serial.available() > 0) {
    // Read the incoming command from Python
    char command = Serial.read();

    // Execute the corresponding movement based on the command
    switch (command) {
      case 'F':  // Move forward
        moveForward();
        break;
      case 'B':  // Move backward
        moveBackward();
        break;
      case 'L':  // Turn left
        turnLeft();
        break;
      case 'R':  // Turn right
        turnRight();
        break;
      case 'S':  // Stop
        stopCar();
        break;
    }
  }
}

// Function to move the car forward
void moveForward() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

// Function to move the car backward
void moveBackward() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
}

// Function to turn the car left
void turnLeft() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

// Function to turn the car right
void turnRight() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
}

// Function to stop the car
void stopCar() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
}
