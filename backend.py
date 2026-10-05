from fastapi import FastAPI
from pydantic import BaseModel, Field
from pecora_engine import scenario_corpus, goal_probability, decision_stress_score, explanation

app = FastAPI(title="PECORA Decision Intelligence API", version="1.0.0")

class AnalyzeRequest(BaseModel):
    name: str = "Investor"
    age: int = Field(default=20, ge=18, le=100)
    goal: str = "Wealth creation"
    goal_amount: float = Field(default=1500000, gt=0)
    current_corpus: float = Field(default=300000, ge=0)
    monthly_sip: float = Field(default=5000, ge=0)
    horizon_years: int = Field(default=6, ge=1, le=50)
    risk_profile: str = "Moderate"
    decision: str = "Continue SIP"
    market_move_pct: float = -4.8
    portfolio_move_pct: float = -4.2

@app.get("/")
def root():
    return {"service": "PECORA Decision Intelligence API", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    projected = scenario_corpus(req.current_corpus, req.monthly_sip, req.horizon_years, req.decision)
    gap = max(req.goal_amount - projected, 0)
    probability = goal_probability(projected, req.goal_amount, req.risk_profile, req.decision)
    stress = decision_stress_score(req.market_move_pct, req.portfolio_move_pct, req.horizon_years, req.risk_profile, gap)
    confidence = max(0.55, min(0.94, 0.82 - abs(req.market_move_pct) / 100 + (0.04 if req.horizon_years >= 5 else 0)))
    return {
        "decision": req.decision,
        "projected_corpus": round(projected, 2),
        "goal_gap": round(gap, 2),
        "goal_probability": round(probability, 4),
        "decision_stress_score": round(stress, 2),
        "ai_confidence": round(confidence, 4),
        "explanation": explanation(req.decision),
        "disclaimer": "Illustrative prototype output, not investment advice."
    }
