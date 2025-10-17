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

    def test_fluxo(self):
        """
        Cenário base: todas as condições normais.
        Valida o comportamento padrão do sistema.
        """
        result = self.run_auxiliar()
        assert result.energy_saving_mode is False
        assert result.temperature_regulation_active is False
        assert all(result.device_status[d] for d in self.default_priorities)

    def test_econ_ativo(self):
        """
        Preço atual excede o limite.
        Sistema ativa economia e desliga dispositivos não essenciais.
        """
        result = self.run_auxiliar(current_price=0.50)
        assert result.energy_saving_mode is True
        assert result.device_status["Microwave"] is False
        assert result.device_status["Sound System"] is False
        assert result.device_status["Security"] is True

    def test_frio(self):
        """
        Temperatura abaixo do mínimo.
        Sistema ativa aquecimento.
        """
        result = self.run_auxiliar(current_temperature=17)
        assert result.temperature_regulation_active is True
        assert isinstance(result.device_status, dict)

    def test_calor(self):
        """
        Temperatura acima do máximo.
        Sistema ativa resfriamento.
        """
        result = self.run_auxiliar(current_temperature=26)
        assert result.temperature_regulation_active is True
        assert isinstance(result.device_status, dict)

    def test_limite_igual(self):
        """
        Consumo diário atinge o limite.
        Sistema desliga ao menos um dispositivo de baixa prioridade,
        mas mantém dispositivos essenciais operando.
        """
        result = self.run_auxiliar(total_energy_used_today=110)
        low_priority = [d for d, p in self.default_priorities.items() if p > 1]
        assert any(result.device_status[d] is False for d in low_priority)
        assert result.device_status["Security"] is True
        assert result.device_status["Refrigerator"] is True

    def test_economia_e_agendamento(self):
        """
        Modo economia ativo com dispositivo agendado.
        Valida que agendamento sobrescreve o modo economia.
        """
        schedule = [
            DeviceSchedule(device_name="Microwave", scheduled_time=datetime(2025, 11, 2, 11, 45))
        ]
        result = self.run_auxiliar(current_price=0.50, scheduled_devices=schedule)
        assert result.energy_saving_mode is True
        assert result.device_status["Microwave"] is True

    def test_agendamento_horario_invalido(self):
        """
        Agendamento existe mas horário não corresponde ao atual.
        """
        schedule = [
            DeviceSchedule(device_name="Microwave", scheduled_time=datetime(2025, 11, 2, 12, 0))
        ]
        result = self.run_auxiliar(scheduled_devices=schedule)
        assert result.device_status["Microwave"] is True

    def test_noturno_e_agendamento(self):
        """
        Horário noturno com agendamento.
        Valida que dispositivo é ligado.
        """
        schedule = [
            DeviceSchedule(device_name="Sound System", scheduled_time=datetime(2025, 11, 2, 4, 0))
        ]
        result = self.run_auxiliar(
            current_time=datetime(2025, 11, 2, 4, 0),
            scheduled_devices=schedule
        )
        assert result.device_status["Sound System"] is True

    def test_limite_ultrapassado(self):
        """
        Consumo diário excede o limite.
        Sistema deve desligar todos dispositivos não essenciais.
        """
        result = self.run_auxiliar(total_energy_used_today=155)
        assert result.device_status["Microwave"] is False
        assert result.device_status["Sound System"] is False
        assert result.device_status["Security"] is True
        assert result.device_status["Refrigerator"] is True