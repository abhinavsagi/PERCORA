EXPECTED_ANNUAL_RETURN = 0.10

def projected_corpus(current_corpus, monthly_sip, horizon_years, annual_return=EXPECTED_ANNUAL_RETURN):
    months = max(1, int(horizon_years * 12))
    r = annual_return / 12
    if r == 0:
        return current_corpus + monthly_sip * months
    return current_corpus * (1 + r) ** months + monthly_sip * (((1 + r) ** months - 1) / r)

def scenario_corpus(current_corpus, monthly_sip, horizon_years, decision):
    months = max(1, int(horizon_years * 12))
    r = EXPECTED_ANNUAL_RETURN / 12

    if decision == "Continue SIP":
        return projected_corpus(current_corpus, monthly_sip, horizon_years)

    if decision == "Pause SIP":
        pause = min(6, months)
        remaining = months - pause
        growth = current_corpus * (1 + r) ** months
        contributions = monthly_sip * (((1 + r) ** remaining - 1) / r) if remaining else 0
        return growth + contributions

    return current_corpus * (1 + r) ** months

def goal_probability(projected, target, risk_profile, decision):
    if target <= 0:
        return 1.0
    ratio = projected / target
    base = max(0.05, min(0.95, ratio))
    risk_adj = {"Conservative": 0.03, "Moderate": 0.0, "Aggressive": -0.03}.get(risk_profile, 0)
    decision_adj = {"Continue SIP": 0.04, "Pause SIP": 0.0, "Stop SIP": -0.05}.get(decision, 0)
    return max(0.02, min(0.98, base * 0.75 + 0.15 + risk_adj + decision_adj))

def decision_stress_score(market_move_pct, portfolio_move_pct, horizon_years, risk_profile, goal_gap):
    market_component = min(abs(market_move_pct) / 10, 1) * 35
    portfolio_component = min(abs(portfolio_move_pct) / 10, 1) * 25
    horizon_component = max(0, min(1, (7 - horizon_years) / 7)) * 20
    risk_component = {"Conservative": 12, "Moderate": 8, "Aggressive": 5}.get(risk_profile, 8)
    gap_component = min(max(goal_gap, 0) / 1000000, 1) * 8
    return max(0, min(100, market_component + portfolio_component + horizon_component + risk_component + gap_component))

def explanation(decision):
    if decision == "Pause SIP":
        return "A pause can reduce the number of contributions working toward your goal. PECORA shows the trade-off before you confirm."
    if decision == "Stop SIP":
        return "Stopping future contributions changes your goal trajectory. PECORA helps you compare that impact with continuing."
    return "Continuing keeps your current contribution path active. PECORA shows the projected trade-off so you can decide with context."
