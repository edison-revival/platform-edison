#include <Arduino.h>
#include <elapsedMillis.h>

// Global timers: their constructors call millis() and micros() before setup(), even
// before main(), which used to crash Intel's core.
elapsedMillis sinceStart;
elapsedMillis sinceBlink;
elapsedMicros sinceStartMicros;

void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    if (sinceBlink >= 500) {
        sinceBlink = 0;
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
        Serial.print("ms since start: ");
        Serial.print((unsigned long)sinceStart);
        Serial.print(", us: ");
        Serial.println((unsigned long)sinceStartMicros);
    }
}
