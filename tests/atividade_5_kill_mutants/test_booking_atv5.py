import pytest
from datetime import datetime, timedelta
from src.flight.FlightBookingSystem import FlightBookingSystem
from src.flight.BookingResult import BookingResult

class TestFlightBookingSystem:

  def setup_method(self):
    self.flight_system = FlightBookingSystem()
    
  # Mutante 17
  def test_booking_exact_available_seats(self):
    result = self.flight_system.book_flight(
      passengers=5,
      booking_time=datetime(2025, 10, 16, 10, 0, 0),
      available_seats=5,
      current_price=100,
      previous_sales=50,
      is_cancellation=False,
      departure_time=datetime(2025, 10, 18, 10, 0, 0),
      reward_points_available=0
    )
    assert result.confirmation == True
  
  # Mutante 36
  def test_group_discount_exactly_4_passengers(self):
    result = self.flight_system.book_flight(
      passengers=4,
      booking_time=datetime(2025, 10, 16, 10, 0, 0),
      available_seats=10,
      current_price=100,
      previous_sales=50,
      is_cancellation=False,
      departure_time=datetime(2025, 10, 18, 10, 0, 0),
      reward_points_available=0
    )
    expected_price = 100 * 0.4 * 4
    assert result.total_price == expected_price
  
  # Mutante 42
  def test_reward_points_exactly_1(self):
    result = self.flight_system.book_flight(
      passengers=1,
      booking_time=datetime(2025, 10, 16, 10, 0, 0),
      available_seats=10,
      current_price=100,
      previous_sales=50,
      is_cancellation=False,
      departure_time=datetime(2025, 10, 18, 10, 0, 0),
      reward_points_available=1
    )
    assert result.points_used == True

  # Mutante 50
  def test_final_price_between_0_and_1(self):
    result = self.flight_system.book_flight(
      passengers=1,
      booking_time=datetime(2025, 10, 16, 10, 0, 0),
      available_seats=10,
      current_price=100,
      previous_sales=50,
      is_cancellation=False,
      departure_time=datetime(2025, 10, 18, 10, 0, 0),
      reward_points_available=3950
    )
    assert result.total_price > 0
    assert result.total_price < 1
  
  # Mutante 53, 54
  def test_cancellation_exactly_48_hours(self):
    booking_time = datetime(2025, 10, 16, 10, 0, 0)
    departure_time = booking_time + timedelta(hours=48)
    result = self.flight_system.book_flight(
      passengers=1,
      booking_time=booking_time,
      available_seats=10,
      current_price=100,
      previous_sales=50,
      is_cancellation=True,
      departure_time=departure_time,
      reward_points_available=0
    )
    expected_price = 100 * 0.4 * 1
    assert result.refund_amount == expected_price