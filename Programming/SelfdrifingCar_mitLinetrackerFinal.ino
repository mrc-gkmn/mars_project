// motor one = Links
int enA = 6;
int in1 = 10;
int in2 = 9;
// motor two = Rechts
int enB = 5;
int in3 = 8;
int in4 = 7;
// Ultraschallsensor:
int trigPin = 11;
int echoPin = 12;
// Ultraschallsensor2:
int trigPin2 = 4;
int echoPin2 = 3;
// Linetracker:
int SensorLinks = 13; // Deklaration des Sensor-Eingangspin
int SensorRechts = 2;

const int Solldistanz = 15;
const int Fahrgeschwindigkeit = 130;
const int AbtastUltraschall = 12; //ms
const int maxGeschwindigkeit = 170;
const int minGeschwindigkeit= 5;
const int FahrgeschwindigkeitLinetrack = 90;
float duration;
float distance;
bool Bande;
float bandenerkennung;
float distanzBande;

void setup()
{
  // set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode (SensorLinks, INPUT) ; // Initialisierung Sensorpin
  pinMode (SensorRechts, INPUT) ;
  Serial.begin(115200);
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  
}

//___________________________________________________________________________________

void entfernungsmessen()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(AbtastUltraschall);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  Serial.print("Distance: ");
  Serial.println(distance);

  
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(AbtastUltraschall);
  digitalWrite(trigPin2, LOW);
  duration = pulseIn(echoPin2, HIGH);
  distanzBande = duration * 0.034 / 2;
  if (distanzBande < 50){
    Bande = HIGH;
    Serial.println("Bande HIGH");
  }
  else {
    Bande = LOW;
    Serial.println("Bande LOW");
    Serial.print(distanzBande);
  }
}
//___________________________________________________________________________________

void starkRechts(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in4, HIGH);
  digitalWrite(in3, LOW);
  Serial.println("Modus: stark Rechts");
  
  analogWrite(enA, maxGeschwindigkeit);
  analogWrite(enB, maxGeschwindigkeit);
}

void starkLinks(){
  digitalWrite(in2, HIGH);
  digitalWrite(in1, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  Serial.println("Modus: stark Links");
  
  analogWrite(enA, maxGeschwindigkeit);
  analogWrite(enB, maxGeschwindigkeit);
}

void geradeaus(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  Serial.print("Modus: Geradeaus");
  
  analogWrite(enA, FahrgeschwindigkeitLinetrack);
  analogWrite(enB, FahrgeschwindigkeitLinetrack);
}

void loop()
{
  entfernungsmessen();

  float antriebRechts = Fahrgeschwindigkeit + 10*(distance - Solldistanz);
  float antriebLinks = Fahrgeschwindigkeit - 10*(distance - Solldistanz);

  if(Bande == HIGH){
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
    if (distance <= (Solldistanz +4) and distance >= (Solldistanz - 4)){ 
      analogWrite(enA, antriebLinks);
      analogWrite(enB, antriebRechts);
      Serial.print("Die Geschwindigkeit Rechts ist: ");
      Serial.println(antriebRechts);
      Serial.print("Die Geschwindigkeit links ist: ");
      Serial.println(antriebLinks);    
    }
    
    else if (distance > (Solldistanz + 4)){
      analogWrite(enB, Fahrgeschwindigkeit -80);
      analogWrite(enA, Fahrgeschwindigkeit +50);
      Serial.print("Die Geschwindigkeit Rechts ist: ");
      Serial.println(Fahrgeschwindigkeit -80);
      Serial.print("Die Geschwindigkeit Links ist: ");
      Serial.println(Fahrgeschwindigkeit +50);
    }
    else {
      analogWrite(enB, Fahrgeschwindigkeit +50);
      analogWrite(enA, Fahrgeschwindigkeit -80);
      Serial.print("Die Geschwindigkeit Rechts ist: ");
      Serial.println(Fahrgeschwindigkeit +50);
      Serial.print("Die Geschwindigkeit Links ist: ");
      Serial.println(Fahrgeschwindigkeit -80);
    }
  }
  else {
    if (digitalRead(SensorLinks) == HIGH) // Falls ein Signal erkannt werden konnte, wird die LED eingeschaltet.
      {    
        starkLinks();
      }
      else if (digitalRead(SensorRechts) == HIGH)
      {
        starkRechts();
      }
      else
      {
        geradeaus();
      }
      //delay(1); // Pasuse zwischen der Messung von 500ms
    }
}
