#include "Arduino.h"
#include "pPump.h"

pPump::pPump(int stepPin, int dirPin, int buttonPin, int period) {
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    pinMode(buttonPin, INPUT);
    _stepPin = stepPin;
    _dirPin = dirPin;
    _buttonPin = buttonPin;
    _period = period;
}                                                                  

void accelerationStepper(int initial, int last, int increment, int stepPin) {
    for(int period = initial; period >= last; period = period - increment) {
        for(int x = 0; x < 20; x++) {                                         //20 steps per incremental period is optimal (stalling < 20 < too slow)
            digitalWrite(stepPin, HIGH);
            delayMicroseconds(period);
            digitalWrite(stepPin, LOW);
            delayMicroseconds(period);
        }
    }
}

double MillToRev(double Mill, int period) {
    return 1.5*Mill - ((1000 - period) * 0.02);
}

void constantStepper(double inMill, int period, int stepPin) {
    for(double i = 0; i < MillToRev(inMill, period); i += 0.1) {       
        for(int z = 0; z < 20; z++) {                          //was previously z < 200 to run for 1 revolution, but changing to 20 gives higher resolution 
            digitalWrite(stepPin, HIGH);
            delayMicroseconds(period);
            digitalWrite(stepPin, LOW);
            delayMicroseconds(period);
        }
    }
}

void primeLoop(int period, int stepPin) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(period);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(period);
}

//pumps a specificed (in milliliters) ammount of liquid
void pPump::pour(double inMill) {
    _inMill = inMill;
    int _initial = 1000;
    int _increment = 5;
    digitalWrite(_dirPin, HIGH);
    accelerationStepper(_initial, _period, _increment, _stepPin);
    constantStepper(_inMill, _period, _stepPin);
}

//funtion designated for pre-filling (priming) the tube with liquid
void pPump::primedrain() {
    int primePeriod = 1000;
    int button = 0;
    int drainRevs = 20;  //placeholder
    button = digitalRead(_buttonPin);
    if (button == HIGH) {
        delay(500);
        button = digitalRead(_buttonPin);
        if (button == HIGH) {
            while (button == HIGH) {
                digitalWrite(_dirPin, HIGH);
                primeLoop(primePeriod, _stepPin);
                button = digitalRead(_buttonPin);
            }
        } else {
            digitalWrite(_dirPin, LOW);
            for (int i = 0; i < drainRevs; i++) {
                for (int y = 0; y < 200; y++) {
                    primeLoop(primePeriod, _stepPin);
                }
            }
        }
    }
}
