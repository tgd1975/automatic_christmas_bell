// pio test -e native: the countdown of lib/BellTimer with made-up millis() values
#include <unity.h>

#include "BellTimer.h"

static const uint32_t RING_MS = 4830;  // six bell swings, as in main.cpp
static const uint32_t T0 = 1000;

void setUp() {}
void tearDown() {}

static uint8_t led(int i) { return (uint8_t)(1 << i); }

void test_idle_after_power_up() {
  BellTimer t(65, RING_MS);
  TEST_ASSERT_EQUAL(BellTimer::IDLE, t.state());
  TEST_ASSERT_EQUAL_UINT32(0, t.remainingMs(T0));
  TEST_ASSERT_EQUAL_UINT8(BellTimer::ALL_LEDS, t.leds(T0));
}

void test_countdown_warning_ring_idle() {
  BellTimer t(65, RING_MS);
  t.start(T0);
  t.update(T0);
  TEST_ASSERT_EQUAL(BellTimer::COUNTDOWN, t.state());
  TEST_ASSERT_EQUAL_UINT32(65000, t.remainingMs(T0));
  // 60 s countdown: 12 s per LED
  TEST_ASSERT_EQUAL(0, t.phase(T0 + 11999));
  TEST_ASSERT_EQUAL(1, t.phase(T0 + 12000));
  TEST_ASSERT_EQUAL(4, t.phase(T0 + 59999));
  t.update(T0 + 59999);
  TEST_ASSERT_EQUAL(BellTimer::COUNTDOWN, t.state());
  t.update(T0 + 60000);
  TEST_ASSERT_EQUAL(BellTimer::WARNING, t.state());
  TEST_ASSERT_EQUAL_UINT32(5000, t.remainingMs(T0 + 60000));
  t.update(T0 + 64999);
  TEST_ASSERT_EQUAL(BellTimer::WARNING, t.state());
  t.update(T0 + 65000);
  TEST_ASSERT_EQUAL(BellTimer::RINGING, t.state());
  TEST_ASSERT_EQUAL_UINT8(0, t.leds(T0 + 65000));
  t.update(T0 + 65000 + RING_MS - 1);
  TEST_ASSERT_EQUAL(BellTimer::RINGING, t.state());
  t.update(T0 + 65000 + RING_MS);
  TEST_ASSERT_EQUAL(BellTimer::IDLE, t.state());
  TEST_ASSERT_EQUAL_UINT8(0, t.leds(T0 + 65000 + RING_MS));  // after the bell: all off
}

void test_countdown_led_blinks() {
  BellTimer t(65, RING_MS);
  t.start(T0);
  uint32_t at = T0 + 12500;  // phase 1; 13500 / 500 is odd: blink on
  TEST_ASSERT_EQUAL_UINT8(led(1), t.leds(at));
  TEST_ASSERT_EQUAL_UINT8(0, t.leds(at + 500));
}

void test_pause_holds_and_resume_goes_on() {
  BellTimer t(65, RING_MS);
  t.start(T0);
  t.update(T0 + 20000);
  t.pause(T0 + 20000);
  TEST_ASSERT_EQUAL(BellTimer::PAUSED, t.state());
  TEST_ASSERT_EQUAL_UINT32(45000, t.remainingMs(T0 + 90000));
  t.update(T0 + 500000);  // a long pause changes nothing
  TEST_ASSERT_EQUAL(BellTimer::PAUSED, t.state());
  TEST_ASSERT_EQUAL_UINT8(led(1), t.leds(T0 + 500000));  // steady, phase 1 (20 s of 12 s per LED)
  TEST_ASSERT_EQUAL_UINT8(led(1), t.leds(T0 + 500500));
  t.start(T0 + 600000);  // start while paused: go on
  TEST_ASSERT_EQUAL(BellTimer::COUNTDOWN, t.state());
  TEST_ASSERT_EQUAL_UINT32(45000, t.remainingMs(T0 + 600000));
  t.update(T0 + 645000);
  TEST_ASSERT_EQUAL(BellTimer::RINGING, t.state());
}

void test_pause_in_final_warning() {
  BellTimer t(65, RING_MS);
  t.start(T0);
  t.update(T0 + 62000);
  TEST_ASSERT_EQUAL(BellTimer::WARNING, t.state());
  t.pause(T0 + 62000);
  TEST_ASSERT_EQUAL_UINT8(BellTimer::ALL_LEDS, t.leds(T0 + 62000));
  t.start(T0 + 70000);
  TEST_ASSERT_EQUAL(BellTimer::WARNING, t.state());
  TEST_ASSERT_EQUAL_UINT32(3000, t.remainingMs(T0 + 70000));
}

void test_pause_only_while_counting() {
  BellTimer t(65, RING_MS);
  t.pause(T0);
  TEST_ASSERT_EQUAL(BellTimer::IDLE, t.state());
  t.ringNow(T0);
  t.pause(T0 + 100);
  TEST_ASSERT_EQUAL(BellTimer::RINGING, t.state());
}

void test_stop_from_anywhere() {
  BellTimer t(65, RING_MS);
  t.start(T0);
  t.stop();
  TEST_ASSERT_EQUAL(BellTimer::IDLE, t.state());
  TEST_ASSERT_EQUAL_UINT8(BellTimer::ALL_LEDS, t.leds(T0));
  t.start(T0);
  t.pause(T0 + 1000);
  t.stop();
  TEST_ASSERT_EQUAL(BellTimer::IDLE, t.state());
  t.start(T0 + 2000);  // after a stop, start begins afresh
  TEST_ASSERT_EQUAL_UINT32(65000, t.remainingMs(T0 + 2000));
}

void test_start_restarts_a_running_countdown() {
  BellTimer t(65, RING_MS);
  t.start(T0);
  t.start(T0 + 30000);
  TEST_ASSERT_EQUAL_UINT32(65000, t.remainingMs(T0 + 30000));
}

void test_ring_now() {
  BellTimer t(65, RING_MS);
  t.ringNow(T0);
  TEST_ASSERT_EQUAL(BellTimer::RINGING, t.state());
  t.update(T0 + RING_MS);
  TEST_ASSERT_EQUAL(BellTimer::IDLE, t.state());
}

void test_set_timer_range_and_next_start() {
  BellTimer t(65, RING_MS);
  TEST_ASSERT_FALSE(t.setTimer(9));
  TEST_ASSERT_FALSE(t.setTimer(24UL * 3600 + 1));
  TEST_ASSERT_EQUAL_UINT32(65, t.timerS());
  t.start(T0);
  TEST_ASSERT_TRUE(t.setTimer(600));
  TEST_ASSERT_EQUAL_UINT32(65000, t.remainingMs(T0));  // the running countdown keeps its time
  t.stop();
  t.start(T0 + 1000);
  TEST_ASSERT_EQUAL_UINT32(600000, t.remainingMs(T0 + 1000));
  TEST_ASSERT_EQUAL(0, t.phase(T0 + 1000));
  TEST_ASSERT_EQUAL(4, t.phase(T0 + 1000 + 594999));
}

void test_bad_timer_falls_back() {
  BellTimer t(3, RING_MS);
  TEST_ASSERT_EQUAL_UINT32(65, t.timerS());
}

void test_millis_overflow() {
  BellTimer t(65, RING_MS);
  uint32_t start = 0xFFFFFFFFUL - 10000;  // 10 s before millis() wraps
  t.start(start);
  t.update(start + 30000);  // wrapped
  TEST_ASSERT_EQUAL(BellTimer::COUNTDOWN, t.state());
  TEST_ASSERT_EQUAL_UINT32(35000, t.remainingMs(start + 30000));
  t.update(start + 65000);
  TEST_ASSERT_EQUAL(BellTimer::RINGING, t.state());
}

int main() {
  UNITY_BEGIN();
  RUN_TEST(test_idle_after_power_up);
  RUN_TEST(test_countdown_warning_ring_idle);
  RUN_TEST(test_countdown_led_blinks);
  RUN_TEST(test_pause_holds_and_resume_goes_on);
  RUN_TEST(test_pause_in_final_warning);
  RUN_TEST(test_pause_only_while_counting);
  RUN_TEST(test_stop_from_anywhere);
  RUN_TEST(test_start_restarts_a_running_countdown);
  RUN_TEST(test_ring_now);
  RUN_TEST(test_set_timer_range_and_next_start);
  RUN_TEST(test_bad_timer_falls_back);
  RUN_TEST(test_millis_overflow);
  return UNITY_END();
}
