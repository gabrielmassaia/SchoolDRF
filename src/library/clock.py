from __future__ import annotations

from datetime import date, timedelta


class Clock:
    def hoje(self) -> date:
        return date.today()


class FixedClock(Clock):
    def __init__(self, data_inicial: date):
        self._data = data_inicial

    def hoje(self) -> date:
        return self._data

    def avancar(self, dias: int = 1) -> None:
        self._data = self._data + timedelta(days=dias)

