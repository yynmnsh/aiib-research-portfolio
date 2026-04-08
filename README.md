# Research & Analytics (Corporate) Intern Portfolio — AIIB Economics Department

**Yayan Puji Riyanto**
PhD Candidate, Business Law & Taxation — Monash University ||
MS Business Analytics — University of Colorado Boulder ||
IT Governance & Regulatory Analyst, DG Tax — Ministry of Finance, Indonesia (2019–2022)

---

## About This Portfolio

This portfolio demonstrates geospatial analysis, causal inference, and data visualization skills relevant to the **Economics Department (ECON)** at AIIB — directly supporting research outputs like Country Net-Zero Reports and the Asian Infrastructure Finance (AIF) Report.

---

## Portfolio Artefacts

### Core Research Demonstrations

| # | Artefact | What It Shows | Platform | Link |
|---|----------|---------------|----------|------|
| 1 | **Satellite Nighttime Lights → Economic Activity** | Geospatial data processing, NTL–GDP elasticity estimation, DiD causal impact of AIIB infrastructure, event study, subnational inequality, infrastructure priority scoring. 12 countries × 178 regions × 10 years. Folium dark-tile maps, PyDeck 3D columns, heatmaps. | Google Colab | [Open Notebook](https://colab.research.google.com/drive/1tXbLXERRtemKe3PAERpPzWweuw_tzZiN?usp=sharing) |
| 2 | **Causal Inference Toolkit** | Four identification strategies: DiD (event study + 1,000 placebo permutations + heterogeneity by quartile), RDD (McCrary test + bandwidth sensitivity), IV/2SLS (first-stage F + bias correction), Synthetic Control (in-space placebo). All with bootstrap inference and publication-grade 4-panel figures. | Google Colab | [Open Notebook](https://colab.research.google.com/drive/1OiFkHnMGvTkh031PM9jYU7SPaVuPl3ul?usp=sharing) |
| 3 | **AIIB Project Portfolio Dashboard** | Interactive visualization of 260 projects across 20 member countries. Scatter geo + choropleth maps, sector treemap, annual trends, Paris alignment tracking, co-financing analysis with leverage ratios. Full sidebar filtering. | Streamlit | [Open App](STREAMLIT_URL_PORTFOLIO) |
| 4 | **Country Net-Zero Analysis: Indonesia** | 6-sector emissions decomposition, 4 NDC scenario pathways (BAU to Net-Zero 2060), 20-province carbon intensity mapping, energy transition trajectories, composite investment priority scoring with radar profiles, 5 AIIB-specific investment recommendations. | Streamlit | [Open App](https://aiib-netzero.streamlit.app/) |

### Research Methodology Showcase

| # | Artefact | What It Shows | Platform | Link |
|---|----------|---------------|----------|------|
| 5 | **PhD Research Brief: Crypto Tax Compliance** | Mixed-methods research design (experiment + survey N=220 + interviews), SEM/CFA, triadic Slippery Slope Framework, compliance behaviour theory — demonstrates econometric and research methodology skills. | Streamlit | [Open App](https://phd-research-brief.streamlit.app/) |

*Note: Artefact #5 is shared with the Operational Risk Intern portfolio — it demonstrates transferable research and analytical skills.*

---

## JD Coverage Map

### Responsibilities

| JD Responsibility | Artefact(s) |
|---|---|
| Process & analyze large geospatial and survey datasets | Satellite Nightlights (1,780 region-year panel, folium/pydeck maps, heatmaps) |
| Conduct analysis using causal inference, ML, and advanced statistics | Causal Inference Toolkit (DiD, RDD, IV, SCM — each with full diagnostics) |
| Develop indicators of welfare & economic activity from satellite imagery | NTL → GDP proxy, capital primacy index, nightlight Gini, infrastructure priority score |
| Document methodology & produce visualisations (maps, charts) | Publication-grade 4-panel figures, dark satellite aesthetic, formatted HTML regression tables, interactive dashboards |
| Contribute in drafting research notes/reports | Country Net-Zero Analysis (full research report structure with policy recommendations for AIIB) |

### Requirements

| JD Requirement | Evidence |
|---|---|
| Enrolled in Masters/PhD in economics, data science, statistics, or related | PhD in Business Law & Taxation (Monash) + MS Business Analytics (CU Boulder) |
| Relevant experience in international organizations or research institutions | 3 years at Indonesia Ministry of Finance (DG Tax), regulatory framework design and implementation |
| Proficiency in Python, R, Stata | All artefacts built in Python — pandas, numpy, sklearn, scipy, plotly, matplotlib, folium, pydeck, streamlit |
| Data management, statistical/econometric analysis skills | OLS with bootstrap CI, DiD, RDD, IV/2SLS, Synthetic Control, SEM/CFA, permutation tests — all demonstrated |
| Geospatial analysis & data science | Folium dark-tile maps, PyDeck 3D columns, nightlight heatmaps, choropleth, scatter_geo — 6+ map types across portfolio |
| Passion for international development | Country Net-Zero analysis with AIIB-specific recommendations; PhD on tax compliance in developing economy |
| Excellent communication | IELTS 8.5; 4 publications; all artefacts in English with professional documentation |

---

## Technical Capabilities Demonstrated

| Category | Tools & Methods |
|---|---|
| **Geospatial** | folium (dark tiles, heatmaps, circle markers), pydeck (3D column maps), Plotly scatter_geo, choropleth |
| **Econometrics** | OLS, DiD, Event Study, RDD (local linear), IV/2SLS, Synthetic Control, SEM/CFA |
| **Statistical Inference** | Bootstrap SE (2,000 iterations), permutation placebo (1,000 iterations), McCrary density test, bandwidth sensitivity, Shapiro-Wilk normality |
| **Data Visualization** | Plotly (interactive charts, treemaps, radar), Matplotlib (publication 4-panel figures, dark theme), Streamlit dashboards |
| **Languages** | Python (primary), R, Stata, SPSS, SQL |
| **ML/Data Science** | scikit-learn, feature engineering, anomaly detection, TF-IDF, StandardScaler |
| **Development Economics** | NDC scenario analysis, NTL-GDP elasticity, infrastructure priority scoring, Paris alignment tracking, climate finance |

---

## Artefact Details

### 1. Satellite Nighttime Lights → Economic Activity
- **Data:** 12 AIIB Asian member countries, 178 subnational regions, 2015–2024 panel
- **Maps:** Folium dark-tile (clickable popups, AIIB project halos), PyDeck 3D columns (rotatable), nightlight density heatmap, Plotly choropleth, animated scatter evolution
- **Econometrics:** NTL–GDP elasticity with 2,000 bootstrap iterations and 95% CI; country-level heterogeneity with per-country bootstrap CI error bars; income group analysis
- **Causal inference:** DiD estimating AIIB infrastructure impact on nightlight intensity, event study with pre-trend validation, parallel trends plot
- **Inequality:** Nightlight Gini coefficient, capital primacy ratio, infrastructure investment priority scoring with tier classification

### 2. Causal Inference Toolkit
- **DiD:** Road construction → regional GDP (200 regions × 11 years). 4 panels: parallel trends, event study, heterogeneity by baseline GDP quartile (bootstrap CI), 1,000-permutation placebo test with p-value
- **RDD:** IDA eligibility threshold → development outcomes (300 countries). 4 panels: main RDD plot with discontinuity arrow, McCrary density test, bandwidth sensitivity across 16 bandwidths, bootstrap distribution
- **IV/2SLS:** Geographic remoteness → trade → growth (150 countries). 4 panels: first-stage with F-statistic, OLS vs 2SLS bias comparison, reduced form, bootstrap distribution
- **SCM:** Special Economic Zone → provincial GDP (16 provinces, 2010–2024). 4 panels: target vs synthetic counterfactual, treatment effect gap, donor weights, in-space placebo test

### 3. AIIB Project Portfolio Dashboard
- **Data:** 260 synthetic projects across 20 AIIB member countries (calibrated to public disclosures)
- **Maps:** Dark satellite scatter geo (switchable color: sector/status/region/Paris), country choropleth
- **Analytics:** Annual approvals trend (dual-axis), sector treemap, regional donut, sector evolution stacked bar, top 10 recipients
- **Climate:** Paris alignment trajectory with 2023 commitment line, alignment by sector and region, climate finance volume trend
- **Co-financing:** Partner breakdown, instrument mix, mobilisation leverage by sector

### 4. Country Net-Zero Analysis: Indonesia
- **Emissions:** 6-sector stacked area (2010–2050), 4 NDC scenario pathways, indexed sector trajectories, sector pie breakdown
- **Infrastructure:** 20-province carbon intensity map, Java vs outer islands scatter, RE penetration by province with national target line
- **Energy:** RE capacity stacked area (solar/wind/geothermal/hydro/biomass), RE share trajectory with RUEN and Net-Zero targets, RE mix donut
- **Investment:** Composite priority score (4 factors), full province ranking with tier classification, radar profiles for top 5, 5 specific AIIB investment recommendations

### 5. PhD Research Brief
- Triadic SSF framework, mixed-methods design, SEM/CFA, compliance modality comparison — demonstrating transferable research methodology skills

---

## Repository Structure

```
aiib-research-portfolio/
├── README.md                                          ← This file
├── nightlights/
│   └── satellite_nightlights_economic_activity.ipynb   ← Satellite NTL analysis
├── causal_inference/
│   └── causal_inference_toolkit.ipynb                  ← 4-method CI toolkit
├── aiib_portfolio/
│   ├── app.py                                          ← Project Portfolio Dashboard
│   └── requirements.txt
├── netzero/
│   ├── app.py                                          ← Country Net-Zero Analysis
│   └── requirements.txt
└── phd_brief/
    └── (linked from OR portfolio)
```

---

## Publications

| Title | Venue | Year | Status |
|-------|-------|------|--------|
| Indonesia's Challenges in Crypto-Asset Tax Regulation | Springer (Book Chapter) | 2026 | In Press |
| The Role of Legal Theory in the Era of Digital Globalization | Jurnal Pembangunan Hukum Indonesia, Vol. 7(2) | 2025 | Published |
| How Do (Tax) Researchers Perceive Crypto? A Systematic Literature Review | Journal of the Australasian Tax Teachers Association, Vol. 19 | 2024 | Published |
| Tax Compliance through Prefilled Forms in a Laboratory Experiment | Scientax, Vol. 5(2) | 2024 | Published |

---

## Contact

- **Email:** yayan.riyanto@monash.edu
- **Phone:** +61 402 460 353
- **LinkedIn:** [linkedin.com/in/yayan-riyanto-a06481b2](https://linkedin.com/in/yayan-riyanto-a06481b2)

---

*This portfolio was prepared for the AIIB Research and Analytics (Corporate) Intern position*
*Economics Department — Asian Infrastructure Investment Bank, Beijing*
