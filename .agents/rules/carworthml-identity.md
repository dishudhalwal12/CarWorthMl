---
trigger: always_on
---

# CarWorthML Visual Identity — Global Rule
# Save to: ~/.gemini/GEMINI.md (or add as Global Rule in Antigravity)

## ACTIVATION: Always On

---

## Identity

This project is CarWorthML — a used car price prediction web application.
It is a BCA Major Project for JEMTEC, Greater Noida.
It runs locally with `streamlit run app.py`.

**Student:** Abhishek Gupta | Enrolment: 01425502022  
**Guide:** Dr. Ruchi Agarwal | Course: BCA VI Sem | Session: 2022–2025

---

## Color System — NEVER CHANGE THESE VALUES

```
BG_PRIMARY    #0A0A0F   Near-black base (Vercel-style)
BG_CARD       #111118   Card backgrounds
BG_ELEVATED   #18181F   Inputs, elevated surfaces
BG_BORDER     #222230   All borders

ACCENT_RED    #E63946   Primary CTA, active states, highlights
TEXT_PRIMARY  #F4F4F5   Main text
TEXT_SECONDARY #8B8B9A  Labels, captions, muted content
TEXT_MUTED    #4A4A5A   Very muted — dividers, footer text

SUCCESS       #22C55E
WARNING       #F59E0B
INFO          #3B82F6
```

If you are ever tempted to use a different color — do not. Use the closest value from this list.

---

## Typography Rules

- Font stack: `-apple-system, 'SF Pro Display', 'Inter', BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Hero heading: `3.4rem, weight 800, letter-spacing -0.05em`
- Section heading: `1.8rem, weight 700, letter-spacing -0.03em`
- Card heading: `1rem, weight 600`
- Body: `0.88–0.95rem, line-height 1.7`
- Labels/captions: `0.75–0.8rem, weight 600, letter-spacing 0.06em, UPPERCASE`

---

## Tab Names — Exact Spelling Required

```
tab1 = "🏠  Home"
tab2 = "🔮  Predict"
tab3 = "📊  Explainatory"    ← intentional spelling, do NOT correct
tab4 = "ℹ️  About"
```

---

## Component Rules

**Cards:** Always use gradient background `linear-gradient(145deg, #18181F, #111118)` with border `1px solid #222230` and `border-radius: 16px`.

**Buttons:** Background `#E63946`, hover `#CC2F3B`, box-shadow `0 4px 15px rgba(230,57,70,0.25)`.

**Tab active state:** Background `#E63946`, glow `0 0 20px rgba(230,57,70,0.3)`.

**Price result card:** Red border `1px solid #E63946`, glow `0 0 40px rgba(230,57,70,0.12)`.

**No white backgrounds anywhere.** If any element shows white, override it with CSS.

---

## What This App Is NOT

- Not a cloud SaaS — runs locally only
- Not using Random Forest or XGBoost — Linear Regression only (synopsis requirement)
- Not using Firebase or any external database
- Not using any authentication system

---

## Definition of Done

The app is only done when:
1. `streamlit run app.py` starts with zero errors
2. All 4 tabs load and render without white backgrounds
3. Predict tab returns a price in realistic INR range
4. R² ≥ 0.75 printed in terminal after model training
5. No placeholders, no TODOs, no "coming soon" text anywhere