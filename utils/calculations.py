from utils.styles import SUCCESS, WARNING, DANGER, TEXT_SECONDARY

def calc_gross_margin(aov, cogs):
    gm = aov - cogs
    gm_pct = (gm / aov * 100) if aov else 0.0
    return gm, gm_pct

def calc_contribution_margin_full(aov, cogs, variable_costs):
    cm = aov - cogs - variable_costs
    cm_pct = (cm / aov * 100) if aov else 0.0
    return cm, cm_pct

def calc_cac(ad_spend, new_orders):
    return (ad_spend / new_orders) if new_orders else 0.0

def calc_ltv(aov, gm_pct, purchases_per_year, lifespan):
    return aov * (gm_pct / 100) * purchases_per_year * lifespan

def calc_ltv_cac_ratio(ltv, cac):
    return (ltv / cac) if cac else 0.0

def calc_breakeven_cac(cm):
    return cm

def calc_target_roas(cm_pct):
    return (100 / cm_pct) if cm_pct else 0.0

def calc_breakeven_orders(fixed_costs, cm_per_order):
    return (fixed_costs / cm_per_order) if cm_per_order else 0.0

_THRESHOLDS = {
    "GM%": [(">", 45, SUCCESS), (">", 35, WARNING)],
    "CM%": [(">", 30, SUCCESS), (">", 20, WARNING)],
    "LTV_CAC": [(">", 3, SUCCESS), (">", 2, WARNING)],
    "ROAS": [(">", 3, SUCCESS), (">", 2, WARNING)],
    "Operating_profit_pct": [(">", 10, SUCCESS), (">", 0, WARNING)],
    "Refund_rate": [("<", 8, SUCCESS), ("<", 12, WARNING)],
}

def health_color(metric, value):
    rules = _THRESHOLDS.get(metric)
    if not rules:
        return TEXT_SECONDARY
    for operator, threshold, color in rules:
        if operator == ">" and value > threshold:
            return color
        if operator == "<" and value < threshold:
            return color
    return DANGER
