#include "BellTimer.h"

BellTimer::BellTimer(uint32_t timerS, uint32_t ringMs) : timerS_(timerS), ringMs_(ringMs) {
  if (!setTimer(timerS)) {
    timerS_ = 65;
  }
}

void BellTimer::start(uint32_t now) {
  if (state_ == PAUSED) {
    dingAt_ = now + pausedMs_;
    state_ = pausedFrom_;
    return;
  }
  runMs_ = timerS_ * 1000;
  dingAt_ = now + runMs_;
  state_ = COUNTDOWN;
}

void BellTimer::pause(uint32_t now) {
  if (state_ != COUNTDOWN && state_ != WARNING) {
    return;
  }
  pausedMs_ = remainingMs(now);
  pausedFrom_ = state_;
  state_ = PAUSED;
}

void BellTimer::stop() {
  state_ = IDLE;
  idleLedsOn_ = true;
}

void BellTimer::ringNow(uint32_t now) {
  state_ = RINGING;
  ringStart_ = now;
}

bool BellTimer::setTimer(uint32_t s) {
  if (s < MIN_TIMER_S || s > MAX_TIMER_S) {
    return false;
  }
  timerS_ = s;
  return true;
}

void BellTimer::update(uint32_t now) {
  if (state_ == COUNTDOWN && remainingMs(now) <= WARNING_MS) {
    state_ = WARNING;
  }
  if (state_ == WARNING && remainingMs(now) == 0) {
    state_ = RINGING;
    ringStart_ = now;
  }
  if (state_ == RINGING && now - ringStart_ >= ringMs_) {
    state_ = IDLE;
    idleLedsOn_ = false;
  }
}

const char *BellTimer::stateName(State s) {
  switch (s) {
    case COUNTDOWN: return "countdown";
    case WARNING: return "warning";
    case PAUSED: return "paused";
    case RINGING: return "ringing";
    default: return "idle";
  }
}

uint32_t BellTimer::remainingMs(uint32_t now) const {
  switch (state_) {
    case COUNTDOWN:
    case WARNING: {
      int32_t left = (int32_t)(dingAt_ - now);  // signed difference: right across the millis() overflow
      return left > 0 ? (uint32_t)left : 0;
    }
    case PAUSED:
      return pausedMs_;
    default:
      return 0;
  }
}

int BellTimer::phase(uint32_t now) const {
  uint32_t left = remainingMs(now);
  if (runMs_ <= WARNING_MS || left <= WARNING_MS) {
    return NUM_LEDS - 1;
  }
  uint32_t countdownMs = runMs_ - WARNING_MS;
  uint32_t elapsed = runMs_ - left;
  int p = (int)((uint64_t)elapsed * NUM_LEDS / countdownMs);
  return p < NUM_LEDS ? p : NUM_LEDS - 1;
}

uint8_t BellTimer::leds(uint32_t now) const {
  bool blinkOn = (now / BLINK_MS) % 2;
  switch (state_) {
    case IDLE:
      return idleLedsOn_ ? ALL_LEDS : 0;
    case COUNTDOWN:
      return blinkOn ? (uint8_t)(1 << phase(now)) : 0;
    case WARNING:
      return blinkOn ? ALL_LEDS : 0;
    case PAUSED:  // steady instead of blinking
      return pausedFrom_ == WARNING ? ALL_LEDS : (uint8_t)(1 << phase(now));
    default:
      return 0;
  }
}
