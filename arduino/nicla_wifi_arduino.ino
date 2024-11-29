#include "Arduino.h"
#include "Arduino_BHY2.h"

void setup(){
  // put your setup code here, to run once:
  BHY2.begin(NICLA_I2C, NICLA_VIA_ESLOV);
}

void loop() {
  // put your main code here, to run repeatedly:
  BHY2.update(1);
}
