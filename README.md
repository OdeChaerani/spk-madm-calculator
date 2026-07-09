# MADM Decision Support Calculator

A web-based **Multi-Attribute Decision Making (MADM)** calculator developed using **Python** and **Streamlit**. This application helps users evaluate and rank alternatives based on multiple criteria using four popular decision-making methods:

- Simple Additive Weighting (SAW)
- Weighted Product (WP)
- Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)
- Analytic Hierarchy Process (AHP)

The application provides an interactive interface for defining criteria, alternatives, weights, and comparison matrices, then automatically calculates the final rankings.

---

## Features

### Supported MADM Methods

- **Simple Additive Weighting (SAW)**
  - Benefit & Cost criteria
  - Weighted normalization
  - Alternative ranking

- **Weighted Product (WP)**
  - Multiplicative weighting
  - Benefit & Cost support
  - Alternative ranking

- **TOPSIS**
  - Vector normalization
  - Positive & Negative Ideal Solutions
  - Preference score calculation
  - Alternative ranking

- **Analytic Hierarchy Process (AHP)**
  - Pairwise comparison matrix
  - Automatic criteria weights
  - Local and global priority calculation
  - Consistency Ratio (CR) evaluation
  - Alternative ranking

---

## User Interface

The application provides an interactive web interface built with Streamlit where users can:

- Select the MADM method
- Define the number of criteria
- Define the number of alternatives
- Enter custom criteria names
- Enter custom alternative names
- Specify Benefit or Cost criteria
- Input criteria weights (SAW, WP, TOPSIS)
- Fill decision matrices
- Create pairwise comparison matrices (AHP)
- Display ranking results
- Highlight the best alternative automatically

---

## Project Structure

```
.
├── app.py
├── metode/
│   ├── ahp.py
│   ├── saw.py
│   ├── topsis.py
│   └── wp.py
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.9+
- Streamlit
- Pandas

Install all dependencies:

```bash
pip install -r requirements.txt
```

or

```bash
pip install streamlit pandas
```

---

## Running the Application

Run the following command:

```bash
streamlit run app.py
```

The application will automatically open in your browser.

---

## Example Workflow

1. Choose a MADM method.
2. Enter the number of criteria and alternatives.
3. Input criteria and alternative names.
4. Fill in weights or comparison matrices.
5. Click **Hitung**.
6. View the ranking results.

---

## Technologies

- Python
- Streamlit
- Pandas

---

## Decision-Making Methods

| Method | Supported |
|---------|-----------|
| SAW | ✅ |
| WP | ✅ |
| TOPSIS | ✅ |
| AHP | ✅ |

---

## Authors

- Wa Ode Zachra Chaerani
- Maritza Ratnamaya N.
