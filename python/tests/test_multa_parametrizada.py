import pytest


@pytest.mark.parametrize(
    "dias_atraso, esperado",
    [
        (0, 0),
        (1, 2.5),
        (3, 7.5),
        (5, 12.5),
    ],
)
def test_calcular_multa_parametrizado(service, dias_atraso, esperado):
    assert service.calcular_multa(dias_atraso) == pytest.approx(esperado)


@pytest.mark.parametrize("dias_atraso", [-1, -10])
def test_calcular_multa_rejeita_atraso_negativo(service, dias_atraso):
    with pytest.raises(ValueError):
        service.calcular_multa(dias_atraso)

