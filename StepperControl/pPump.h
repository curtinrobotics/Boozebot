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
