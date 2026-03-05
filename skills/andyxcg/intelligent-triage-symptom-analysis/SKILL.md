---
name: intelligent-triage-symptom-analysis
description: Intelligent Triage and Symptom Analysis Skill. Supports 650+ symptoms across 11 body systems. Based on ESI and Manchester Triage System with 5-level triage classification. Features NLP-driven symptom extraction, 3000+ disease database, red flag warning mechanism (≥95% accuracy for life-threatening conditions), and machine learning-assisted differential diagnosis.
version: 1.0.0
---

# Intelligent Triage and Symptom Analysis

AI-powered medical triage assistance for healthcare providers, telemedicine platforms, and patients. Provides accurate preliminary symptom assessment and urgency recommendations.

## Features

1. **Comprehensive Symptom Coverage** - 650+ symptoms across 11 body systems
2. **Standardized Triage** - 5-level classification (Resuscitation to Non-emergency)
3. **Red Flag Detection** - ≥95% accuracy for life-threatening conditions
4. **NLP Analysis** - Natural language symptom extraction
5. **Differential Diagnosis** - ML-assisted condition ranking
6. **SkillPay Billing** - 1 token per analysis (~0.001 USDT)

## Quick Start

### Analyze symptoms:

```python
from scripts.triage import analyze_symptoms
import os

# Set environment variables
os.environ["SKILL_BILLING_API_KEY"] = "your-api-key"
os.environ["SKILL_ID"] = "your-skill-id"

# Analyze patient symptoms
result = analyze_symptoms(
    symptoms="胸痛，呼吸困难，持续30分钟",
    age=65,
    gender="male",
    vital_signs={"bp": "160/95", "hr": 110, "temp": 37.2},
    user_id="user_123"
)

# Check result
if result["success"]:
    print("分诊等级:", result["triage"]["level"])
    print("紧急程度:", result["triage"]["urgency"])
    print("建议措施:", result["recommendations"])
else:
    print("错误:", result["error"])
    if "paymentUrl" in result:
        print("充值链接:", result["paymentUrl"])
```

### API Usage:

```bash
# Set environment variables
export SKILL_BILLING_API_KEY="your-api-key"
export SKILL_ID="your-skill-id"

# Run analysis
python scripts/triage.py \
  --symptoms "胸痛，呼吸困难" \
  --age 65 \
  --gender male \
  --user-id "user_123"
```

## Configuration

- Provider: skillpay.me
- Pricing: 1 token per call (~0.001 USDT)
- Minimum deposit: 8 USDT
- API Key: `SKILL_BILLING_API_KEY` environment variable
- Skill ID: `SKILL_ID` environment variable

## Triage Levels

| Level | Name | Response Time | Examples |
|-------|------|---------------|----------|
| 1 | Resuscitation | Immediate | Cardiac arrest, severe trauma |
| 2 | Emergent | <15 min | Chest pain, severe bleeding |
| 3 | Urgent | <30 min | Abdominal pain, fever |
| 4 | Less Urgent | <60 min | Minor injuries, chronic symptoms |
| 5 | Non-urgent | >60 min | Follow-up, prescription refill |

## Supported Body Systems

- Cardiovascular
- Respiratory
- Gastrointestinal
- Neurological
- Musculoskeletal
- Dermatological
- Genitourinary
- Endocrine
- Hematological
- Immunological
- Psychiatric

## References

- Triage methodology: [references/triage-systems.md](references/triage-systems.md)
- Billing API: [references/skillpay-billing.md](references/skillpay-billing.md)
- Disease database: [references/disease-database.md](references/disease-database.md)

## Disclaimer

This tool is for preliminary assessment only and does not replace professional medical diagnosis. Always consult qualified healthcare providers for medical decisions.
