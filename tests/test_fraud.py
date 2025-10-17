import pytest
from datetime import datetime, timedelta
from src.fraud.Transaction import Transaction
from src.fraud.FraudDetectionSystem import FraudDetectionSystem


class TestFraudDetectionStructural:
    
    def setup_method(self):
        self.fraud_system = FraudDetectionSystem()
    
    
    # TESTE 1: Transação Normal - Sem quebrar nenhuma regra
    def test_normal_transaction(self):
        """
        Resultado esperado:
        - is_fraudulent = False
        - is_blocked = False
        - verification_required = False
        - risk_score = 0
        """
        current_transaction = Transaction(
            amount=100.00,
            location='Brasil',
            timestamp=datetime(2025, 10, 16, 14, 0, 0)
        )
        previous_transactions = []
        blacklisted_locations = []
        
        result = self.fraud_system.check_for_fraud(
            current_transaction,
            previous_transactions,
            blacklisted_locations
        )
        
        assert result.is_fraudulent == False
        assert result.is_blocked == False
        assert result.verification_required == False
        assert result.risk_score == 0
    
    
    # TESTE 2: Valor Alto - Regra 1
    def test_high_value_transaction(self):
        """
        Resultado esperado:
        - is_fraudulent = True
        - is_blocked = False
        - verification_required = True
        - risk_score = 50
        """
        current_transaction = Transaction(
            amount=15000.00,
            location='Brasil',
            timestamp=datetime(2025, 10, 16, 14, 0, 0)
        )
        previous_transactions = []
        blacklisted_locations = []
        
        result = self.fraud_system.check_for_fraud(
            current_transaction,
            previous_transactions,
            blacklisted_locations
        )
        
        assert result.is_fraudulent == True
        assert result.is_blocked == False
        assert result.verification_required == True
        assert result.risk_score == 50
    
    
    # TESTE 3: Muitas Transações Recentes - Regra 2
    def test_excessive_transactions(self):
        """
        Resultado esperado:
        - is_fraudulent = False
        - is_blocked = True
        - verification_required = False
        - risk_score = 30
        """
        base_time = datetime(2025, 10, 16, 13, 0, 0)
        previous_transactions = []
        for i in range(11):
            previous_transactions.append(
                Transaction(
                    amount=50.00,
                    location='Brasil',
                    timestamp=base_time + timedelta(minutes=i*5)
                )
            )
        
        current_transaction = Transaction(
            amount=100.00,
            location='Brasil',
            timestamp=datetime(2025, 10, 16, 14, 0, 0)
        )
        blacklisted_locations = []
        
        result = self.fraud_system.check_for_fraud(
            current_transaction,
            previous_transactions,
            blacklisted_locations
        )
        
        assert result.is_fraudulent == False
        assert result.is_blocked == True
        assert result.verification_required == False
        assert result.risk_score == 30
    
    
    # TESTE 4: Mudança Rápida de Localização - Regra 3
    def test_rapid_location_change(self):
        """
        Resultado esperado:
        - is_fraudulent = True
        - is_blocked = False
        - verification_required = True
        - risk_score = 20
        """
        previous_transactions = [
            Transaction(
                amount=50.00,
                location='EUA',
                timestamp=datetime(2025, 10, 16, 13, 40, 0)
            )
        ]
        
        current_transaction = Transaction(
            amount=100.00,
            location='Brasil',
            timestamp=datetime(2025, 10, 16, 14, 0, 0)
        )
        blacklisted_locations = []
        
        result = self.fraud_system.check_for_fraud(
            current_transaction,
            previous_transactions,
            blacklisted_locations
        )
        
        assert result.is_fraudulent == True
        assert result.is_blocked == False
        assert result.verification_required == True
        assert result.risk_score == 20
    
    
    # TESTE 5: Local na Blacklist - Regra 4
    def test_blacklisted_location(self):
        """
        Resultado esperado:
        - is_fraudulent = False
        - is_blocked = True
        - verification_required = False
        - risk_score = 100
        """
        current_transaction = Transaction(
            amount=100.00,
            location='Brasil',
            timestamp=datetime(2025, 10, 16, 14, 0, 0)
        )
        previous_transactions = []
        blacklisted_locations = ['Brasil']
        
        result = self.fraud_system.check_for_fraud(
            current_transaction,
            previous_transactions,
            blacklisted_locations
        )
        
        assert result.is_fraudulent == False
        assert result.is_blocked == True
        assert result.verification_required == False
        assert result.risk_score == 100
    
    
    # TESTE 6: Valor Alto + Blacklist - Regras 1 e 4
    def test_high_value_and_blacklist(self):
        """
        Resultado esperado:
        - is_fraudulent = True
        - is_blocked = True
        - verification_required = True
        - risk_score = 100 (sobrescreve o 50 anterior)
        """
        current_transaction = Transaction(
            amount=15000.00,
            location='Brasil',
            timestamp=datetime(2025, 10, 16, 14, 0, 0)
        )
        previous_transactions = []
        blacklisted_locations = ['Brasil']
        
        result = self.fraud_system.check_for_fraud(
            current_transaction,
            previous_transactions,
            blacklisted_locations
        )
        
        assert result.is_fraudulent == True
        assert result.is_blocked == True
        assert result.verification_required == True
        assert result.risk_score == 100
    
    
    # TESTE 7: Caso de Borda - 10 Transações e Valor Exatamente 10000
    def test_boundary(self):
        """
        Resultado esperado:
        - is_fraudulent = False
        - is_blocked = False
        - verification_required = False
        - risk_score = 0
        """
        base_time = datetime(2025, 10, 16, 13, 0, 0)
        previous_transactions = []
        for i in range(10):
            previous_transactions.append(
                Transaction(
                    amount=50.00,
                    location='Brasil',
                    timestamp=base_time + timedelta(minutes=i*6)
                )
            )
        
        current_transaction = Transaction(
            amount=10000.00,
            location='Brasil',
            timestamp=datetime(2025, 10, 16, 14, 0, 0)
        )
        blacklisted_locations = []
        
        result = self.fraud_system.check_for_fraud(
            current_transaction,
            previous_transactions,
            blacklisted_locations
        )
        
        assert result.is_fraudulent == False
        assert result.is_blocked == False
        assert result.verification_required == False
        assert result.risk_score == 0

# TESTE 7 modificado para 100% de coverage: Caso de Borda - 10 Transações e Valor Exatamente 10000
    def test_boundary_modified(self):
        """
        Resultado esperado:
        - is_fraudulent = False
        - is_blocked = False
        - verification_required = False
        - risk_score = 0
        """
        base_time = datetime(2025, 10, 16, 13, 0, 0)
        previous_transactions = []

        previous_transactions.append(
            Transaction(
                amount=50.00,
                location='Brasil',
                timestamp=datetime(2025, 10, 16, 12, 0, 0)
            )
        )
        
        for i in range(10):
            previous_transactions.append(
                Transaction(
                    amount=50.00,
                    location='Brasil',
                    timestamp=base_time + timedelta(minutes=i*6)
                )
            )
        
        current_transaction = Transaction(
            amount=10000.00,
            location='Brasil',
            timestamp=datetime(2025, 10, 16, 14, 0, 0)
        )
        blacklisted_locations = []
        
        result = self.fraud_system.check_for_fraud(
            current_transaction,
            previous_transactions,
            blacklisted_locations
        )
        
        assert result.is_fraudulent == False
        assert result.is_blocked == False
        assert result.verification_required == False
        assert result.risk_score == 0