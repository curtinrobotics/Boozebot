/*
* Header file for the pPump Library
* Programmers: CJD
* Editor: 
* Iteration: 0.2
* Last edited: 02/03/2021
* Created: 10/08/2021
* 
* Dependencies: Arduino.h
*/

#ifndef PPUMP_H
#define PPUMP_H

#include "Arduino.h"

class pPump {
    public:
        pPump(int stepPin, int dirPin, int buttonPin, int period);
        void pour(double inMill);
        void primedrain();
    private:
        int _stepPin;
        int _dirPin;
        int _buttonPin;
        int _period;
        double _inMill;
};

#endif
