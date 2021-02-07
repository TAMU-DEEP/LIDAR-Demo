
//www.elegoo.com
#define ENA 5
#define ENB 6
#define IN1 7
#define IN2 8
#define IN3 9
#define IN4 11
#define LED 13

unsigned char carSpeed = 10;
bool state = LOW;
char getstr;

String delimiter = ":";
unsigned long last_command_time;
unsigned long current_time;
const unsigned long period = 1000;

#define INPUT_SIZE 30


//run right wheels
void right_wheels(int speed){ 
  bool forward = true;
  if (speed < 0) forward = false;
  speed = abs(speed);
  
  analogWrite(ENA,speed);
  if (forward) {
    digitalWrite(IN1,HIGH);
    digitalWrite(IN2,LOW);
  } else {
    digitalWrite(IN1,LOW);
    digitalWrite(IN2,HIGH);   
  }
}

//run left wheels
void left_wheels(int speed){ 
  bool forward = true;
  if (speed < 0) forward = false;
  speed = abs(speed);
  
  analogWrite(ENB,speed);
  if (forward) {
    digitalWrite(IN3,LOW);
    digitalWrite(IN4,HIGH);
  } else {
    digitalWrite(IN3,HIGH);
    digitalWrite(IN4,LOW);   
  }
}

void read_command(){
  char input[INPUT_SIZE + 1];
   byte size = Serial.readBytes(input, INPUT_SIZE);
   // Add the final 0 to end the C string
   input[size] = 0;
  

  // Read each command pair 
  char* command = strtok(input, "&");
  while (command != 0)
  { 
    // Split the command in two values
    char* separator = strchr(command, ':');
    if (separator != 0)
    {
        // Actually split the string in 2: replace ':' with 0
        *separator = 0;
        int left = atoi(command);
        ++separator;
        int right = atoi(separator);

        left  = min(left, 255);
        right = min(right, 255);

        right_wheels(right);
        left_wheels(left);
        
    }
    // Find the next command in input string
    command = strtok(0, "&");
  } 
  
}

void forward(){ 
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,HIGH);
  //Serial.println("Forward");
}

void back(){
  digitalWrite(ENA,HIGH);
  digitalWrite(ENB,HIGH);
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
  //Serial.println("Back");
}

void left(){
  analogWrite(ENA,carSpeed);
  analogWrite(ENB,carSpeed);
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,HIGH); 
  //Serial.println("Left");
}

void right(){
  analogWrite(ENA,carSpeed);
  analogWrite(ENB,carSpeed);
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
  //Serial.println("Right");
}

void stop(){
  digitalWrite(ENA,LOW);
  digitalWrite(ENB,LOW);
  //Serial.println("Stop!");
}

void stateChange(){
  state = !state;
  digitalWrite(LED, state);
  //Serial.println("Light");  
}
