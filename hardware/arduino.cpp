char t;
char previous = 'A';
bool firstDetection = true;
bool avoidObstacle = false;

const int ldrPin = A0;
const int ledPin = 4;
const int threshold = 500;

const int frontTrig = 3;
const int frontEcho = A2;
const int backTrig = 5;
const int backEcho = A3; 

const int buzzer = A5;

void setup(){
  pinMode(2,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(frontTrig, OUTPUT);
  pinMode(frontEcho, INPUT);
  pinMode(backTrig, OUTPUT);
  pinMode(backEcho, INPUT);
  pinMode(buzzer, OUTPUT);
  
  Serial.begin(9600);
}

long measureDistance(int trigPin, int echoPin){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long duration = pulseIn(echoPin, HIGH);
    long distance = duration * 0.034 / 2;
    return distance;
}

void loop(){
  if(Serial.available()){
    t = Serial.read();
  }
  
  //not efficient and not necessary
  if (t != previous){
    digitalWrite(2,HIGH);
    delay(50);
    digitalWrite(2,LOW);
  }
  
  if (t != '0'){
    previous = t;
  }
  
  bool avoidObstacle = true;
  
  long frontDistance = measureDistance(frontTrig, frontEcho);
  long backDistance = measureDistance(backTrig, backEcho);
  
  Serial.println(digitalRead(buzzer));
  
  int ldrValue = analogRead(ldrPin);
  Serial.println(ldrValue);

  if (ldrValue < threshold){
    digitalWrite(ledPin, HIGH);
  } 
  else{
    digitalWrite(ledPin, LOW);
  }
  
  
  if (t == 'F'){
    if (frontDistance > 20 && backDistance > 20){
      digitalWrite(6,HIGH);
      digitalWrite(7,LOW);
      digitalWrite(8,HIGH);
      digitalWrite(9,LOW);
      digitalWrite(10,HIGH);
      digitalWrite(11,LOW);
      digitalWrite(12,HIGH);
      digitalWrite(13,LOW);
      avoidObstacle = false;
    }
  }
  if (t == 'B'){
      digitalWrite(6,LOW);
      digitalWrite(7,HIGH);
      digitalWrite(8,LOW);
      digitalWrite(9,HIGH);
      digitalWrite(10,LOW);
      digitalWrite(11,HIGH);
      digitalWrite(12,LOW);
      digitalWrite(13,HIGH);
      avoidObstacle = false;
  }
  if (t == 'L'){
    if (frontDistance > 20){
      digitalWrite(6,LOW);
      digitalWrite(7,HIGH);
      digitalWrite(8,LOW);
      digitalWrite(9,HIGH);
      digitalWrite(10,HIGH);
      digitalWrite(11,LOW);
      digitalWrite(12,HIGH);
      digitalWrite(13,LOW);
      avoidObstacle = false;
    }
  }
  if (t == 'R'){
    if (backDistance > 20){
      digitalWrite(6,HIGH);
      digitalWrite(7,LOW);
      digitalWrite(8,HIGH);
      digitalWrite(9,LOW);
      digitalWrite(10,LOW);
      digitalWrite(11,HIGH);
      digitalWrite(12,LOW);
      digitalWrite(13,HIGH);
      avoidObstacle = false;
    }
  }
  if (t == 'S'){
      digitalWrite(6,LOW);
      digitalWrite(7,LOW);
      digitalWrite(8,LOW);
      digitalWrite(9,LOW);
      digitalWrite(10,LOW);
      digitalWrite(11,LOW);
      digitalWrite(12,LOW);
      digitalWrite(13,LOW);
      avoidObstacle = false;
  }

  if (frontDistance <= 20 || backDistance <= 20){
	 if (firstDetection || avoidObstacle){
      digitalWrite(6,LOW);
      digitalWrite(7,LOW);
      digitalWrite(8,LOW);
      digitalWrite(9,LOW);
      digitalWrite(10,LOW);
      digitalWrite(11,LOW);
      digitalWrite(12,LOW);
      digitalWrite(13,LOW);
    
      //not efficient cause it stays working for 300ms
      tone(buzzer, 1000);
      digitalWrite(2,HIGH);
      delay(100);
      tone(buzzer, 1200);
      delay(100);
      tone(buzzer, 800);
      digitalWrite(2,LOW);
      delay(100);
      noTone(buzzer);
      
      firstDetection = false;
    }
    else {
      noTone(buzzer);
    }
  } 
  else {
    firstDetection = true;
    t = previous;
  }
}