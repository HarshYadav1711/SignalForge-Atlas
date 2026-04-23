def kelly_fraction(probability: float, b: float = 1.0) -> float:
    """
    Kelly sizing with cap:
      f = (p*(b+1) - 1)/b
    with b fixed to 1 by default and result clipped to [0, 0.2].
    """
    p = max(0.0, min(1.0, float(probability)))
    if b <= 0:
        return 0.0
    raw_fraction = (p * (b + 1.0) - 1.0) / b
    return max(0.0, min(0.2, raw_fraction))
