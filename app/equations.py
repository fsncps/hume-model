import math

def eq_production(A: float, K: float, alpha: float) -> float:
    """Y = A * K^alpha"""
    return A * (K ** alpha)

def eq_consumption(Y: float, s: float, D: float) -> float:
    """C = (1 - s) * Y * D"""
    return (1 - s) * Y * D

def eq_investment(Y: float, s: float, D: float) -> float:
    """I = s * Y * D"""
    return s * Y * D

def eq_output(A: float, K: float, alpha: float) -> float:
    """Y = A * K^alpha"""
    return A * (K ** alpha)


def eq_total_output(C: float, I: float) -> float:
    """Y = C + I"""
    return C + I

def eq_capital_accumulation(K_last: float, I: float, delta: float) -> float:
    """K = (1 - delta) * K_last + I"""
    return (1 - delta) * K_last + I

def eq_profit(alpha: float, Y: float, K: float) -> float:
    """p = alpha * Y / K"""
    return alpha * Y / K

def eq_interest_rate(p: float, gamma: float) -> float:
    """r = p - gamma"""
    return p - gamma

def eq_savings_rate(C: float, Y: float) -> float:
    """s = C / Y"""
    return C / Y

def eq_credit_supply(s: float, Y: float) -> float:
    """K = s * Y"""
    return s * Y

def eq_wealth_concentration(K: float, M: float) -> float:
    """theta = K / M"""
    return K / M

def eq_price_level(M: float, Y: float) -> float:
    """P = M / Y"""
    return M / Y

def eq_inflation(P: float, P_last: float) -> float:
    """pi = P / P(-1) - 1"""
    return P / P_last - 1

def eq_quantity(P: float, Y: float) -> float:
    """MV = PY [V=1]"""
    return P * Y
