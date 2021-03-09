
// touch includes
#include <MPR121.h>
#include <MPR121_Datastream.h>
#include <Wire.h>

// touch constants
const uint32_t BAUD_RATE = 9600;
const uint8_t MPR121_ADDR = 0x5A;  // 0x5C is the MPR121 I2C address on the Bare Touch Board
const uint8_t MPR121_INT = 4;  // pin 4 is the MPR121 interrupt on the Bare Touch Board

// MPR121 datastream behaviour constants
const bool MPR121_DATASTREAM_ENABLE = false;

void setup() {
  Serial.begin(BAUD_RATE);
  Serial.println("Started the sensing");

  if (!MPR121.begin(MPR121_ADDR)) {
    Serial.println("error setting up MPR121");
    switch (MPR121.getError()) {
      case NO_ERROR:
        Serial.println("no error");
        break;
      case ADDRESS_UNKNOWN:
        Serial.println("incorrect address");
        break;
      case READBACK_FAIL:
        Serial.println("readback failure");
        break;
      case OVERCURRENT_FLAG:
        Serial.println("overcurrent on REXT pin");
        break;
      case OUT_OF_RANGE:
        Serial.println("electrode out of range");
        break;
      case NOT_INITED:
        Serial.println("not initialised");
        break;
      default:
        Serial.println("unknown error");
        break;
    }
    while (1);
  }

  MPR121.setInterruptPin(MPR121_INT);

  if (MPR121_DATASTREAM_ENABLE) {
    MPR121.restoreSavedThresholds();
    MPR121_Datastream.begin(&Serial);
  } else {
    MPR121.setTouchThreshold(40);  // this is the touch threshold - setting it low makes it more like a proximity trigger, default value is 40 for touch
    MPR121.setReleaseThreshold(20);  // this is the release threshold - must ALWAYS be smaller than the touch threshold, default value is 20 for touch
  }

  MPR121.setFFI(FFI_10);
  MPR121.setSFI(SFI_10);
  MPR121.setGlobalCDT(CDT_4US);  // reasonable for larger capacitances
  
  digitalWrite(LED_BUILTIN, HIGH);  // switch on user LED while auto calibrating electrodes
  delay(1000);
  MPR121.autoSetElectrodes();  // autoset all electrode settings
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  MPR121.updateAll();
  for (int i = 0; i < 12; i++) {
    if (MPR121.isNewTouch(i)) {
      Serial.print("Touched");
      Serial.print("-");
      Serial.print(i, DEC);
      Serial.print(" ");
    } else if (MPR121.isNewRelease(i)) {
      Serial.print("Released");
      Serial.print("-");
      Serial.print(i, DEC);
      Serial.print(" ");
    }
  }
  Serial.println("");
  if (MPR121_DATASTREAM_ENABLE) {
    MPR121_Datastream.update();
  }
  delay(100);
}
