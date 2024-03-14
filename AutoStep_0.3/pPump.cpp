/*
* This program is contains functions for the pPump library
* Programmers: CJD
* Editor: 
* Iteration: 0.2
* Last edited: 02/03/2021
* Created: 10/08/2021
* 
* Dependencies: pPump.h, Arduino.h
*
* Library contrains fuctions for driving peristaltic pumps as they will be used for Boozebot
* (Will be expanded to include linear rail functions and protothreading in next iteration)
*/

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

/* subfunction used by pour()
    function accelerates stepper motor to its final period
    important to avoid motor stalling */
void accelerationStepper(int initial, int last, int increment, int stepPin) {
    for (int period = initial; period >= last; period = period - increment) {
        for (int x = 0; x < 20; x++) { //20 steps per incremental period is optimal (stalling < 20 < too slow)
            digitalWrite(stepPin, HIGH);
            delayMicroseconds(period);
            digitalWrite(stepPin, LOW);
            delayMicroseconds(period);
        }
    }
}

/* subfunction used by constantStepper()
    function converts recived data (in millimeters) to an 
    appropriate number of revolutions of the stepper motor */
double MillToRev(double Mill, int period) {
    return 1.5 * Mill - ((1000 - period) * 0.02);
}

/* subfunction used by pour()
    function for providing the specified amount of liquid
    by turning the pumps at a constant speed */
void constantStepper(double inMill, int period, int stepPin) {
    for (double i = 0; i < MillToRev(inMill, period); i += 0.1) {

        /* performs a tenth of a revolution every iteration */
        for (int z = 0; z < 20; z++) { 
            digitalWrite(stepPin, HIGH);
            delayMicroseconds(period);
            digitalWrite(stepPin, LOW);
            delayMicroseconds(period);
        }
    }
}

/* subfunction used by primedrain()
    function turns pumps at a constant rate */
void primeLoop(int period, int stepPin) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(period);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(period);
}

/* function pumps a specificed (in milliliters) ammount of liquid */
void pPump::pour(double inMill) {
    _inMill = inMill;
    int _initial = 1000;
    int _increment = 10;
    digitalWrite(_dirPin, HIGH);
    accelerationStepper(_initial, _period, _increment, _stepPin);
    constantStepper(_inMill, _period, _stepPin);
}

/* funtion for priming and draining tubes of liquid */
void pPump::primedrain() {
    int primePeriod = 1000;
    int button = 0;
    int drainRevs = 20; //placeholder
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
