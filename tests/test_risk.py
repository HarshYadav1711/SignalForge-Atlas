from agents.risk_agent import kelly_fraction


def test_kelly_fraction_respects_bounds() -> None:
    assert 0.0 <= kelly_fraction(0.0) <= 0.2
    assert 0.0 <= kelly_fraction(0.25) <= 0.2
    assert 0.0 <= kelly_fraction(0.5) <= 0.2
    assert 0.0 <= kelly_fraction(0.75) <= 0.2
    assert 0.0 <= kelly_fraction(1.0) <= 0.2


def test_kelly_fraction_caps_and_clamps() -> None:
    assert kelly_fraction(-1.0) == 0.0
    assert kelly_fraction(2.0) == 0.2
