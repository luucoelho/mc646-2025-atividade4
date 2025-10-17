import pytest
from datetime import datetime, timedelta
from src.flight.FlightBookingSystem import FlightBookingSystem
from src.flight.BookingResult import BookingResult

class TestFlightBookingSystem:

  def test_insufficient_seats(self): #CT1
    system = FlightBookingSystem()
    result = system.book_flight(
      passengers=5,
      booking_time=datetime(2024, 1, 15, 10, 0),
      available_seats=3,
      current_price=200.0,
      previous_sales=50,
      is_cancellation=False,
      departure_time=datetime(2024, 1, 20, 10, 0),
      reward_points_available=0
    )
    assert result.confirmation == False
    assert result.total_price == 0.0
    assert result.refund_amount == 0.0
    assert result.points_used == False


  def test_normal_booking_no_special_conditions(self): #CT2
    system = FlightBookingSystem()
    result = system.book_flight(
      passengers=2,
      booking_time=datetime(2024, 1, 15, 10, 0),
      available_seats=10,
      current_price=200.0,
      previous_sales=100,  # price_factor = 0.8
      is_cancellation=False,
      departure_time=datetime(2024, 1, 20, 10, 0),  # >24h
      reward_points_available=0
    )
    # final_price = 200 * 0.8 * 2 = 320
    assert result.confirmation == True
    assert result.total_price == 320.0
    assert result.refund_amount == 0.0
    assert result.points_used == False


  def test_last_minute_booking(self): #CT3
    system = FlightBookingSystem()
    result = system.book_flight(
      passengers=2,
      booking_time=datetime(2024, 1, 15, 10, 0),
      available_seats=10,
      current_price=200.0,
      previous_sales=100,
      is_cancellation=False,
      departure_time=datetime(2024, 1, 15, 20, 0),  # 10h difference
      reward_points_available=0
    )
    # final_price = (200 * 0.8 * 2) + 100 = 420
    assert result.confirmation == True
    assert result.total_price == 420.0
    assert result.refund_amount == 0.0
    assert result.points_used == False

  def test_group_discount(self): #CT4
    system = FlightBookingSystem()
    result = system.book_flight(
        passengers=5,  # >4 passengers
        booking_time=datetime(2024, 1, 15, 10, 0),
        available_seats=10,
        current_price=200.0,
        previous_sales=100,
        is_cancellation=False,
        departure_time=datetime(2024, 1, 20, 10, 0),
        reward_points_available=0
    )
    # final_price = (200 * 0.8 * 5) * 0.95 = 760
    assert result.confirmation == True
    assert result.total_price == 760.0
    assert result.refund_amount == 0.0
    assert result.points_used == False

  def test_reward_points(self): #CT5
    system = FlightBookingSystem()
    result = system.book_flight(
        passengers=2,
        booking_time=datetime(2024, 1, 15, 10, 0),
        available_seats=10,
        current_price=200.0,
        previous_sales=100,
        is_cancellation=False,
        departure_time=datetime(2024, 1, 20, 10, 0),
        reward_points_available=5000  # $50 discount
    )
    # final_price = (200 * 0.8 * 2) - 50 = 270
    assert result.confirmation == True
    assert result.total_price == 270.0
    assert result.refund_amount == 0.0
    assert result.points_used == True

  def test_excessive_reward_points(self): #CT6
    system = FlightBookingSystem()
    result = system.book_flight(
        passengers=1,
        booking_time=datetime(2024, 1, 15, 10, 0),
        available_seats=10,
        current_price=100.0,
        previous_sales=100,
        is_cancellation=False,
        departure_time=datetime(2024, 1, 20, 10, 0),
        reward_points_available=20000  # $200 discount
    )
    # final_price = (100 * 0.8 * 1) - 200 = -120 → 0
    assert result.confirmation == True
    assert result.total_price == 0.0
    assert result.refund_amount == 0.0
    assert result.points_used == True

  def test_cancellation_more_than_48h(self): #CT7
    system = FlightBookingSystem()
    result = system.book_flight(
        passengers=2,
        booking_time=datetime(2024, 1, 10, 10, 0),
        available_seats=10,
        current_price=200.0,
        previous_sales=100,
        is_cancellation=True,
        departure_time=datetime(2024, 1, 15, 10, 0),  # 120h difference
        reward_points_available=0
    )
    # refund_amount = final_price = 200 * 0.8 * 2 = 320
    assert result.confirmation == False
    assert result.total_price == 0.0
    assert result.refund_amount == 320.0
    assert result.points_used == False

  def test_cancellation_less_than_48h(self): #CT8
    system = FlightBookingSystem()
    result = system.book_flight(
        passengers=2,
        booking_time=datetime(2024, 1, 10, 10, 0),
        available_seats=10,
        current_price=200.0,
        previous_sales=100,
        is_cancellation=True,
        departure_time=datetime(2024, 1, 11, 10, 0),  # 24h difference
        reward_points_available=0
    )
    # refund_amount = (200 * 0.8 * 2) * 0.5 = 160
    assert result.confirmation == False
    assert result.total_price == 0.0
    assert result.refund_amount == 160.0
    assert result.points_used == False

  def test_zero_previous_sales(self): #CT9
    system = FlightBookingSystem()
    result = system.book_flight(
        passengers=2,
        booking_time=datetime(2024, 1, 15, 10, 0),
        available_seats=10,
        current_price=200.0,
        previous_sales=0,  # price_factor = 0
        is_cancellation=False,
        departure_time=datetime(2024, 1, 20, 10, 0),
        reward_points_available=0
    )
    # final_price = 200 * 0 * 2 = 0
    assert result.confirmation == True
    assert result.total_price == 0.0
    assert result.refund_amount == 0.0
    assert result.points_used == False

  def test_combined_conditions(self): #CT10
    system = FlightBookingSystem()
    result = system.book_flight(
        passengers=5,  # group discount
        booking_time=datetime(2024, 1, 15, 10, 0),
        available_seats=10,
        current_price=200.0,
        previous_sales=50,  # price_factor = 0.4
        is_cancellation=False,
        departure_time=datetime(2024, 1, 15, 20, 0),  # last minute
        reward_points_available=1000  # $10 discount
    )
    # base_price = 200 * 0.4 * 5 = 400
    # + last_minute = 400 + 100 = 500
    # group_discount = 500 * 0.95 = 475
    # reward_points = 475 - 10 = 465
    assert result.confirmation == True
    assert result.total_price == 465.0
    assert result.points_used == True
    assert result.refund_amount == 0.0