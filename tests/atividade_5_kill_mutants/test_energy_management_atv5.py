import pytest
from datetime import datetime
from src.energy.EnergyManagementSystem import SmartEnergyManagementSystem
from src.energy.DeviceSchedule import DeviceSchedule


class TestEnergyManagementStructural:
    """
    Testes Sistema Inteligente de Gestão de Energia.
    Cada teste valida um caminho específico.
    """

    def setup_method(self):
        """Configura prioridades do sistema"""
        self.energy_system = SmartEnergyManagementSystem()
        self.default_priorities = {
            "Security": 1,
            "Refrigerator": 1,
            "Microwave": 2,
            "Sound System": 2,
            "Computer": 2
        }

    def run_auxiliar(self, **overrides):
        """
        Método auxiliar que executa o sistema com parâmetros base, permitindo sobrescrever apenas valores específicos do cenário de teste.
        """
        base_params = dict(
            current_price=0.28,
            price_threshold=0.32,
            current_time=datetime(2025, 11, 2, 11, 45),
            current_temperature=22,
            desired_temperature_range=(20, 24),
            energy_usage_limit=110,
            total_energy_used_today=35,
            device_priorities=self.default_priorities,
            scheduled_devices=[]
        )
        base_params.update(overrides)
        return self.energy_system.manage_energy(**base_params)

    # Mutante 4
    def test_total_energy_used_is_stored(self):
        result = self.run_auxiliar(total_energy_used_today=75)
        
        assert result.total_energy_used == 75
        assert result.total_energy_used is not None
