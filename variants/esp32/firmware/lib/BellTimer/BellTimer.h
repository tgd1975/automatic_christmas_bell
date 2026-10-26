// The countdown of the Christmas bell without hardware: time to ding, pause, stop, timer setting and the LED
// pattern, driven by millis(). The firmware (src/main.cpp) feeds it buttons and web commands and moves servo and
// LEDs; the host tests (test/) drive it with made-up times.
//
// The timer is the time from start to ding. Its last WARNING_MS are the final warning (all LEDs blink); the time
// before is the countdown, shown on the five LEDs green 1, green 2, yellow 1, yellow 2, red – one fifth each,
// blinking. Then the bell rings for ringMs and the bell goes back to idle with all LEDs off.
#pragma once

#include <stdint.h>

class BellTimer {
public:
  enum State { IDLE, COUNTDOWN, WARNING, PAUSED, RINGING };

  static const uint32_t WARNING_MS = 5000;        // final warning before the bell
  static const uint32_t BLINK_MS = 500;           // LEDs toggle every 500 ms
  static const uint32_t MIN_TIMER_S = 10;
  static const uint32_t MAX_TIMER_S = 24UL * 3600;
  static const int NUM_LEDS = 5;
  static const uint8_t ALL_LEDS = (1 << NUM_LEDS) - 1;

  BellTimer(uint32_t timerS, uint32_t ringMs);

  // Commands; now = millis()
  void start(uint32_t now);    // paused: go on; otherwise a fresh countdown with the timer setting
  void pause(uint32_t now);    // countdown or final warning: hold the time to ding
  void stop();                 // back to idle, all LEDs on
  void ringNow(uint32_t now);  // the bell rings at once – start held and reset pressed, as on the Nano (a test)
  bool setTimer(uint32_t s);   // MIN_TIMER_S ... MAX_TIMER_S; counts from the next start

  void update(uint32_t now);   // time-driven transitions; call every loop

  static const char *stateName(State s);  // idle, countdown, warning, paused, ringing – the web page's names

  State state() const { return state_; }
  uint32_t timerS() const { return timerS_; }
  uint32_t remainingMs(uint32_t now) const;  // time to ding; 0 when idle or ringing
  int phase(uint32_t now) const;             // countdown LED 0 ... NUM_LEDS - 1
  uint8_t leds(uint32_t now) const;          // bit i = LED i on

private:
  uint32_t timerS_;
  uint32_t ringMs_;
  State state_ = IDLE;
  State pausedFrom_ = COUNTDOWN;
  bool idleLedsOn_ = true;   // idle after power-up or stop: all on; after the bell: all off
  uint32_t runMs_ = 0;       // timer of the running countdown
  uint32_t dingAt_ = 0;      // millis() of the ding while counting down
  uint32_t pausedMs_ = 0;    // time to ding while paused
  uint32_t ringStart_ = 0;
};
