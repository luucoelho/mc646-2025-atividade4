import pytest
from datetime import datetime, timedelta
from src.fraud.Transaction import Transaction
from src.fraud.FraudDetectionSystem import FraudDetectionSystem


class TestFraudDetectionStructural:
    
    def setup_method(self):
        self.fraud_system = FraudDetectionSystem()
    
    # Mutante 73
    def test_boundary_10001(self):
        current = Transaction(10001.00, datetime(2025, 10, 16, 14, 0, 0), 'Brasil')
        result = self.fraud_system.check_for_fraud(current, [], [])
        assert result.is_fraudulent == True
        assert result.risk_score == 50
    
    # Mutantes 97, 116
    def test_risk_score_accumulation_kills_78_97_116(self):
        base_time = datetime(2025, 10, 16, 13, 0, 0)
        previous = []
        
        for i in range(11):
            previous.append(Transaction(50.00, base_time + timedelta(minutes=i*5), 'Brasil'))
        
        previous.append(Transaction(50.00, datetime(2025, 10, 16, 13, 45, 0), 'EUA'))
        
        current = Transaction(15000.00, datetime(2025, 10, 16, 14, 0, 0), 'Brasil')
        result = self.fraud_system.check_for_fraud(current, previous, [])
        
        assert result.risk_score == 100  # 50 + 30 + 20
    
    # Mutante 86
    def test_exactly_60_minutes_transaction(self):
        previous = [Transaction(100.00, datetime(2025, 10, 16, 13, 0, 0), 'Brasil')]
        current = Transaction(100.00, datetime(2025, 10, 16, 14, 0, 0), 'Brasil')
        result = self.fraud_system.check_for_fraud(current, previous, [])
        assert result.is_blocked == False
    
    # Mutante 89
    def test_transaction_at_61_minutes(self):
        base_time = datetime(2025, 10, 16, 13, 0, 0)
        previous = [Transaction(50.00, base_time + timedelta(minutes=i*5.5), 'Brasil') for i in range(11)]
        current = Transaction(100.00, base_time + timedelta(minutes=61), 'Brasil')
        result = self.fraud_system.check_for_fraud(current, previous, [])
        assert result.is_blocked == False
    
    # Mutantes 106, 108
    def test_location_change_exactly_30_minutes_kills_106_108(self):
        previous = [Transaction(100.00, datetime(2025, 10, 16, 13, 30, 0), 'EUA')]
        current = Transaction(100.00, datetime(2025, 10, 16, 14, 0, 0), 'Brasil')
        result = self.fraud_system.check_for_fraud(current, previous, [])
        
        assert result.is_fraudulent == False
        assert result.risk_score == 0
    
    # Mutante 109
    def test_location_change_at_30_5_minutes_kills_109(self):
        previous = [Transaction(100.00, datetime(2025, 10, 16, 13, 29, 30), 'EUA')]
        current = Transaction(100.00, datetime(2025, 10, 16, 14, 0, 0), 'Brasil')
        result = self.fraud_system.check_for_fraud(current, previous, [])
        
        assert result.is_fraudulent == False
        assert result.risk_score == 0