# SaaS vs Local AI: Cost Comparison Calculator

> Own project by Manu (OpenClaw Labs). Interactive cost calculator built with Streamlit.

## What it does

Compares what you pay for SaaS AI subscriptions with running the same capability on your own server:

- Monthly and yearly cost side by side
- Break-even point
- 3-year total cost of ownership
- Architecture comparison (SaaS vs self-hosted)

The numbers are the ones you enter; the calculator does not assume any savings.

## Quick start

```bash
git clone https://github.com/beastbymanu-ux/saas-replacement-calculator
cd saas-replacement-calculator
pip install -r requirements.txt
streamlit run app.py
```

Or with Docker: `docker build -t saas-calculator . && docker run -p 8501:8501 saas-calculator`

---
*Built by Manu · OpenClaw Labs (my own AI lab)*
