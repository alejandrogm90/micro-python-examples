import importlib
import sys
from types import SimpleNamespace

# Registro de la última instancia creada para inspección
class RegPin:
    OUT = 0
    instances = []

    def __init__(self, pin_num, mode):
        self.pin_num = pin_num
        self.mode = mode
        self.values = []
        RegPin.instances.append(self)

    def value(self, v=None):
        if v is None:
            return self.values[-1] if self.values else None
        self.values.append(v)

# Helper para importar src.Blink con mocks
def import_with_mocks(monkeypatch, mock_pin_cls, mock_sleep):
    if 'Blink' in sys.modules:
        del sys.modules['Blink']
    monkeypatch.setitem(sys.modules, 'machine', SimpleNamespace(Pin=mock_pin_cls))
    monkeypatch.setitem(sys.modules, 'time', SimpleNamespace(sleep_ms=mock_sleep))
    mod = importlib.import_module('Blink')
    return mod


def test_blink_toggles_led_and_calls_sleep(monkeypatch):
    RegPin.instances.clear()
    sleep_calls = []

    def mock_sleep_ms(ms):
        sleep_calls.append(ms)
        if len(sleep_calls) >= 4:
            raise Exception("stop")

    mod = import_with_mocks(monkeypatch, RegPin, mock_sleep_ms)
    mod.example1()

    assert len(RegPin.instances) == 1
    pin = RegPin.instances[0]
    assert pin.values[:4] == [0, 1, 0, 1]
    assert all(ms == 1000 for ms in sleep_calls[:4])

def test_blink_handles_exception_and_exits(monkeypatch):
    RegPin.instances.clear()
    calls = []

    def mock_sleep_ms_once(ms):
        calls.append(ms)
        raise KeyboardInterrupt()

    mod = import_with_mocks(monkeypatch, RegPin, mock_sleep_ms_once)
    mod.example1()

    assert len(RegPin.instances) == 1
    pin = RegPin.instances[0]
    assert pin.values and pin.values[0] == 0
    assert calls and calls[0] == 1000
