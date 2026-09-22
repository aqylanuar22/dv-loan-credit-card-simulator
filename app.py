import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Loan & Credit Card Simulator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background: #FBF8F5;
        }

        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #E8DDE2;
        }

        .hero {
            background: linear-gradient(135deg, #54152B 0%, #800020 100%);
            padding: 32px 36px;
            border-radius: 20px;
            color: white;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(128, 0, 32, 0.14);
        }

        .hero h1 {
            font-size: 38px;
            margin: 0 0 8px 0;
            font-weight: 700;
        }

        .hero p {
            font-size: 16px;
            margin: 0;
            opacity: 0.90;
        }

        .section-title {
            color: #54152B;
            font-size: 24px;
            font-weight: 700;
            margin-top: 8px;
            margin-bottom: 4px;
        }

        .section-description {
            color: #756D73;
            font-size: 14px;
            margin-bottom: 16px;
        }

        .metric-card {
            background: white;
            border: 1px solid #E8DDE2;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 5px 18px rgba(47, 41, 48, 0.05);
            min-height: 115px;
        }

        .metric-label {
            color: #756D73;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .metric-value {
            color: #54152B;
            font-size: 25px;
            font-weight: 750;
        }

        .metric-note {
            color: #9A9297;
            font-size: 12px;
            margin-top: 5px;
        }

        .insight-card {
            background: #FFFFFF;
            border-left: 5px solid #800020;
            border-radius: 14px;
            padding: 18px 20px;
            margin-top: 12px;
            box-shadow: 0 5px 18px rgba(47, 41, 48, 0.05);
        }

        .insight-title {
            color: #54152B;
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .insight-text {
            color: #3F373C;
            font-size: 14px;
            line-height: 1.6;
        }

        .student-card {
            background: #F6E9EE;
            border: 1px solid #E8DDE2;
            border-radius: 14px;
            padding: 15px 16px;
            margin-bottom: 18px;
        }

        .student-name {
            color: #54152B;
            font-size: 18px;
            font-weight: 800;
            letter-spacing: 0.4px;
        }

        .student-id {
            color: #756D73;
            font-size: 12px;
            margin-top: 4px;
        }

        .sidebar-title {
            color: #54152B;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .sidebar-subtitle {
            color: #756D73;
            font-size: 13px;
            line-height: 1.5;
            margin-bottom: 20px;
        }

        .loan-type-note {
            background: #F6E9EE;
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 12.5px;
            color: #54152B;
            margin-top: -6px;
            margin-bottom: 18px;
            line-height: 1.5;
        }

        .affordability-card {
            border-radius: 16px;
            padding: 20px 22px;
            border: 1px solid #E8DDE2;
            box-shadow: 0 5px 18px rgba(47, 41, 48, 0.05);
        }

        .status-badge {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .disclaimer {
            font-size: 12px;
            color: #9A9297;
            margin-top: 6px;
            line-height: 1.5;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAN TYPE PRESETS
# ============================================================
# Typical, illustrative ranges only — real offers vary by bank/lender.

LOAN_PRESETS = {
    "Personal Loan": {
        "icon": "💵",
        "min_amount": 1_000.0, "max_amount": 100_000.0, "default_amount": 20_000.0,
        "min_rate": 3.0, "max_rate": 18.0, "default_rate": 8.0,
        "min_term": 6, "max_term": 120, "default_term": 36,
        "description": (
            "An unsecured loan for personal expenses. Usually has a higher "
            "interest rate and a shorter repayment term than car or house loans."
        )
    },
    "Car Loan": {
        "icon": "🚗",
        "min_amount": 5_000.0, "max_amount": 300_000.0, "default_amount": 80_000.0,
        "min_rate": 2.0, "max_rate": 6.5, "default_rate": 3.5,
        "min_term": 12, "max_term": 108, "default_term": 84,
        "description": (
            "A loan secured against the vehicle you're buying. Interest rates "
            "are typically lower than personal loans, with terms of 5–9 years."
        )
    },
    "House Loan": {
        "icon": "🏠",
        "min_amount": 50_000.0, "max_amount": 2_000_000.0, "default_amount": 350_000.0,
        "min_rate": 2.5, "max_rate": 6.0, "default_rate": 4.0,
        "min_term": 12, "max_term": 420, "default_term": 360,
        "description": (
            "A mortgage secured against property. Usually the lowest interest "
            "rate of the four, but the longest repayment term (often 25–35 years)."
        )
    },
    "Credit Card": {
        "icon": "💳",
        "min_amount": 500.0, "max_amount": 100_000.0, "default_amount": 5_000.0,
        "min_rate": 12.0, "max_rate": 18.0, "default_rate": 15.0,
        "min_term": 1, "max_term": 120, "default_term": 24,
        "description": (
            "Revolving credit rather than a fixed loan. If you only pay the "
            "minimum each month, interest builds up fast and payoff can take "
            "much longer than a personal loan for the same balance."
        )
    }
}


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div class="student-card">
        <div class="student-name">AQIL ANUAR</div>
        <div class="student-id">Student ID: 24000198</div>
    </div>

    <div class="sidebar-title">⚙️ Simulation Settings</div>
    <div class="sidebar-subtitle">
        Choose a borrowing type, adjust the numbers, and see whether
        the monthly payment fits your income.
    </div>
    """,
    unsafe_allow_html=True
)

loan_type = st.sidebar.selectbox(
    "Borrowing Type",
    list(LOAN_PRESETS.keys()),
    format_func=lambda name: f"{LOAN_PRESETS[name]['icon']} {name}"
)

preset = LOAN_PRESETS[loan_type]

st.sidebar.markdown(
    f'<div class="loan-type-note">ℹ️ {preset["description"]}</div>',
    unsafe_allow_html=True
)

amount = st.sidebar.number_input(
    f"{loan_type} Amount (RM)",
    min_value=preset["min_amount"],
    max_value=preset["max_amount"],
    value=preset["default_amount"],
    step=500.0
)

interest_rate = st.sidebar.number_input(
    f"{loan_type} Annual Interest Rate (%)",
    min_value=preset["min_rate"],
    max_value=preset["max_rate"],
    value=preset["default_rate"],
    step=0.1
)

term_months = st.sidebar.number_input(
    f"{loan_type} Repayment Term (months)",
    min_value=preset["min_term"],
    max_value=preset["max_term"],
    value=preset["default_term"],
    step=1
)

payment_behavior = st.sidebar.radio(
    "Payment Behaviour",
    ["On-time", "Early", "Late"],
    index=0
)

st.sidebar.divider()

st.sidebar.markdown(
    '<div class="sidebar-title" style="font-size:16px;">💼 Your Income</div>',
    unsafe_allow_html=True
)

monthly_salary = st.sidebar.number_input(
    "Your Monthly Net Salary (RM)",
    min_value=0.0,
    max_value=1_000_000.0,
    value=3_000.0,
    step=100.0,
    help="Used only to estimate whether this payment is affordable for you. Set to 0 to hide the affordability check."
)

st.sidebar.divider()

st.sidebar.caption(
    "The simulation updates automatically whenever an input changes."
)


# ============================================================
# CALCULATIONS
# ============================================================

monthly_rate = interest_rate / 100 / 12


def calculate_monthly_payment(principal, monthly_interest, months):
    if monthly_interest == 0:
        return principal / months

    return (
        principal
        * monthly_interest
        * (1 + monthly_interest) ** months
        / ((1 + monthly_interest) ** months - 1)
    )


base_payment = calculate_monthly_payment(
    amount,
    monthly_rate,
    term_months
)


if payment_behavior == "On-time":
    monthly_payment = base_payment
    behaviour_description = (
        "The borrower follows the calculated required monthly payment."
    )

elif payment_behavior == "Early":
    monthly_payment = base_payment * 1.25
    behaviour_description = (
        "The borrower pays 25% more than the calculated monthly payment."
    )

else:
    monthly_payment = base_payment * 0.75
    behaviour_description = (
        "The borrower pays 25% less than the calculated monthly payment."
    )


def simulate_repayment(
    principal,
    annual_rate,
    monthly_payment,
    max_months=1000
):
    monthly_interest_rate = annual_rate / 100 / 12

    balance = principal
    month = 0
    total_interest = 0
    total_paid = 0
    records = []

    while balance > 0 and month < max_months:
        month += 1

        interest = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest

        if principal_payment <= 0:
            principal_payment = 0
            actual_payment = interest
        else:
            actual_payment = monthly_payment

        if principal_payment > balance:
            principal_payment = balance
            actual_payment = principal_payment + interest

        balance -= principal_payment

        total_interest += interest
        total_paid += actual_payment

        records.append(
            {
                "Month": month,
                "Payment": actual_payment,
                "Interest": interest,
                "Principal": principal_payment,
                "Remaining Balance": max(balance, 0)
            }
        )

    return pd.DataFrame(records), total_interest, total_paid


schedule, total_interest, total_paid = simulate_repayment(
    amount,
    interest_rate,
    monthly_payment
)

on_time_schedule, on_time_interest, on_time_total = simulate_repayment(
    amount,
    interest_rate,
    base_payment
)

early_schedule, early_interest, early_total = simulate_repayment(
    amount,
    interest_rate,
    base_payment * 1.25
)

late_schedule, late_interest, late_total = simulate_repayment(
    amount,
    interest_rate,
    base_payment * 0.75
)


if payment_behavior == "Early":
    difference = on_time_total - total_paid
    difference_label = "Estimated Savings"

elif payment_behavior == "Late":
    difference = total_paid - on_time_total
    difference_label = "Estimated Extra Cost"

else:
    difference = 0
    difference_label = "Difference from On-time"


# ============================================================
# AFFORDABILITY LOGIC
# ============================================================
# Rule of thumb only (not financial advice): keep total debt repayments
# under roughly 30-35% of net monthly income to stay comfortable.

RECOMMENDED_DTI = 0.30  # 30% used for the "recommended minimum salary" figure

recommended_salary = monthly_payment / RECOMMENDED_DTI if RECOMMENDED_DTI > 0 else 0

has_salary_input = monthly_salary > 0
dti_ratio = (monthly_payment / monthly_salary * 100) if has_salary_input else None


def get_affordability_status(dti):
    if dti <= 30:
        return {
            "label": "Comfortable",
            "color": "#2E7D32",
            "background": "#E8F5E9",
            "message": (
                "This payment fits comfortably within a healthy budget, "
                "leaving room for savings and daily expenses."
            )
        }
    elif dti <= 40:
        return {
            "label": "Manageable",
            "color": "#B8860B",
            "background": "#FFF8E1",
            "message": (
                "This payment is manageable, but it leaves less room for "
                "savings or unexpected expenses. Keep an eye on your budget."
            )
        }
    elif dti <= 50:
        return {
            "label": "Risky",
            "color": "#D2691E",
            "background": "#FFF0E5",
            "message": (
                "This payment takes up a large share of your income. Consider "
                "a smaller amount, a longer term, or increasing your income "
                "before committing."
            )
        }
    else:
        return {
            "label": "Not Recommended",
            "color": "#B00020",
            "background": "#FDE8E8",
            "message": (
                "This payment could put serious strain on your finances. It's "
                "worth reconsidering the loan amount, term, or looking for a "
                "lower-cost option before proceeding."
            )
        }


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <h1>{preset['icon']} {loan_type} Payment Simulator</h1>
        <p>
            Explore how payment behaviour affects repayment time, interest
            cost, and — most importantly — whether it fits your income.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CURRENT SCENARIO
# ============================================================

st.markdown(
    '<div class="section-title">📌 Current Scenario</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="section-description">{behaviour_description}</div>',
    unsafe_allow_html=True
)


# ============================================================
# METRIC CARDS
# ============================================================

metric_columns = st.columns(4)

metrics = [
    (
        "Monthly Payment",
        f"RM {monthly_payment:,.2f}",
        "What you'd pay each month under this behaviour"
    ),
    (
        "Total Interest",
        f"RM {total_interest:,.2f}",
        "Interest paid over the simulated period"
    ),
    (
        "Time to Payoff",
        f"{len(schedule)} months",
        "Estimated repayment duration"
    ),
    (
        difference_label,
        f"RM {difference:,.2f}",
        "Compared with the on-time scenario"
    )
]

for column, (label, value, note) in zip(metric_columns, metrics):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")


# ============================================================
# AFFORDABILITY CHECK
# ============================================================

st.markdown(
    '<div class="section-title">🧭 Can You Afford This?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'A simple check comparing this monthly payment against your income, '
    'using the common guideline of keeping debt repayments under about '
    '30–35% of your net monthly salary.'
    '</div>',
    unsafe_allow_html=True
)

afford_col1, afford_col2 = st.columns([1, 1.2])

with afford_col1:
    st.markdown(
        f"""
        <div class="affordability-card">
            <div class="metric-label">Recommended Minimum Salary</div>
            <div class="metric-value" style="font-size:22px;">RM {recommended_salary:,.2f} / month</div>
            <div class="metric-note">
                To keep this payment at or below a comfortable {int(RECOMMENDED_DTI*100)}% of income.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if has_salary_input:
        status = get_affordability_status(dti_ratio)
        st.markdown(
            f"""
            <div class="affordability-card" style="background:{status['background']};">
                <span class="status-badge" style="background:{status['color']}; color:white;">
                    {status['label']}
                </span>
                <div class="metric-value" style="font-size:22px; color:{status['color']};">
                    {dti_ratio:.1f}% of your salary
                </div>
                <div class="metric-note" style="color:#3F373C;">
                    {status['message']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info(
            "Enter your monthly salary in the sidebar to see a personalised "
            "affordability status."
        )

with afford_col2:
    gauge_value = dti_ratio if has_salary_input else 0
    gauge_color = get_affordability_status(gauge_value)["color"] if has_salary_input else "#9A9297"

    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=gauge_value,
            number={"suffix": "%", "font": {"color": "#54152B"}},
            title={"text": "Debt-to-Income Ratio", "font": {"size": 16, "color": "#3F373C"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#756D73"},
                "bar": {"color": gauge_color},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 30], "color": "#E8F5E9"},
                    {"range": [30, 40], "color": "#FFF8E1"},
                    {"range": [40, 50], "color": "#FFF0E5"},
                    {"range": [50, 100], "color": "#FDE8E8"}
                ],
                "threshold": {
                    "line": {"color": "#54152B", "width": 3},
                    "thickness": 0.8,
                    "value": 35
                }
            }
        )
    )

    fig_gauge.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_gauge, width="stretch")

st.markdown(
    '<div class="disclaimer">'
    '⚠️ This is an educational simulation for general guidance only and is '
    'not financial advice. For a decision specific to your situation, please '
    'speak with a licensed financial advisor or your bank.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# VIEW 1: REMAINING BALANCE
# ============================================================

st.markdown(
    '<div class="section-title">📈 View 1: Repayment Progress</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Track how the outstanding balance changes throughout the repayment period. '
    'The chart updates automatically when the scenario changes.'
    '</div>',
    unsafe_allow_html=True
)

fig_balance = go.Figure()

fig_balance.add_trace(
    go.Scatter(
        x=schedule["Month"],
        y=schedule["Remaining Balance"],
        mode="lines+markers",
        name=payment_behavior,
        line=dict(color="#800020", width=3),
        marker=dict(color="#800020", size=5),
        hovertemplate=(
            "<b>Month %{x}</b><br>"
            "Remaining Balance: RM %{y:,.2f}"
            "<extra></extra>"
        )
    )
)

fig_balance.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=25, b=20),
    paper_bgcolor="white",
    plot_bgcolor="white",
    hovermode="x unified",
    xaxis=dict(
        title=dict(text="Repayment Month", font=dict(size=14, color="#3F373C")),
        showgrid=True,
        gridcolor="#E9E0E4",
        zeroline=False
    ),
    yaxis=dict(
        title=dict(text="Remaining Balance (RM)", font=dict(size=14, color="#3F373C")),
        showgrid=True,
        gridcolor="#E9E0E4",
        zeroline=False,
        tickprefix="RM "
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    )
)

st.plotly_chart(
    fig_balance,
    width="stretch"
)


# ============================================================
# VIEW 2: INTEREST COMPARISON
# ============================================================

st.markdown(
    '<div class="section-title">💹 View 2: Interest Cost Comparison</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Compare the total interest generated by early, on-time and late payment strategies.'
    '</div>',
    unsafe_allow_html=True
)

comparison_data = pd.DataFrame(
    {
        "Payment Behaviour": ["Early", "On-time", "Late"],
        "Total Interest": [
            early_interest,
            on_time_interest,
            late_interest
        ]
    }
)

fig_interest = px.bar(
    comparison_data,
    x="Payment Behaviour",
    y="Total Interest",
    text="Total Interest",
    labels={
        "Payment Behaviour": "Payment Behaviour",
        "Total Interest": "Total Interest (RM)"
    }
)

fig_interest.update_traces(
    marker_color="#800020",
    texttemplate="RM %{y:,.2f}",
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Total Interest: RM %{y:,.2f}"
        "<extra></extra>"
    )
)

fig_interest.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor="white",
    plot_bgcolor="white",
    showlegend=False,
    xaxis=dict(
        title=dict(text="Payment Behaviour", font=dict(size=14, color="#3F373C")),
        showgrid=False
    ),
    yaxis=dict(
        title=dict(text="Total Interest (RM)", font=dict(size=14, color="#3F373C")),
        showgrid=True,
        gridcolor="#E9E0E4",
        zeroline=False,
        tickprefix="RM "
    )
)

st.plotly_chart(
    fig_interest,
    width="stretch"
)


# ============================================================
# VIEW 3: PRINCIPAL VS INTEREST
# ============================================================

st.markdown(
    '<div class="section-title">🥧 View 3: Principal vs Interest</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Break down the total repayment into the original principal and accumulated interest.'
    '</div>',
    unsafe_allow_html=True
)

composition_data = pd.DataFrame(
    {
        "Component": ["Principal", "Interest"],
        "Amount": [amount, total_interest]
    }
)

fig_composition = px.pie(
    composition_data,
    names="Component",
    values="Amount",
    hole=0.55
)

fig_composition.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Amount: RM %{value:,.2f}<br>"
        "Share: %{percent}"
        "<extra></extra>"
    )
)

fig_composition.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="white",
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.05,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(
    fig_composition,
    width="stretch"
)


# ============================================================
# STRATEGY COMPARISON
# ============================================================

st.markdown(
    '<div class="section-title">📋 Strategy Comparison</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'A numerical comparison of the three repayment strategies.'
    '</div>',
    unsafe_allow_html=True
)

strategy_comparison = pd.DataFrame(
    {
        "Payment Behaviour": ["Early", "On-time", "Late"],
        "Monthly Payment (RM)": [
            base_payment * 1.25,
            base_payment,
            base_payment * 0.75
        ],
        "Total Interest (RM)": [
            early_interest,
            on_time_interest,
            late_interest
        ],
        "Total Repaid (RM)": [
            early_total,
            on_time_total,
            late_total
        ],
        "Payoff Period (Months)": [
            len(early_schedule),
            len(on_time_schedule),
            len(late_schedule)
        ]
    }
)

if has_salary_input:
    strategy_comparison["DTI vs Your Salary (%)"] = (
        strategy_comparison["Monthly Payment (RM)"] / monthly_salary * 100
    ).round(1)

for column in [
    "Monthly Payment (RM)",
    "Total Interest (RM)",
    "Total Repaid (RM)"
]:
    strategy_comparison[column] = strategy_comparison[column].round(2)

st.dataframe(
    strategy_comparison,
    width="stretch",
    hide_index=True
)


# ============================================================
# INTERPRETATION
# ============================================================

st.markdown(
    '<div class="section-title">💡 What Does This Scenario Tell Us?</div>',
    unsafe_allow_html=True
)

if payment_behavior == "Early":
    interpretation = (
        f"With early payment, the simulated monthly payment is "
        f"RM {monthly_payment:,.2f}. Paying more each month reduces "
        f"the outstanding balance faster. Compared with the on-time "
        f"scenario, the estimated difference in total repayment is "
        f"RM {difference:,.2f}."
    )

elif payment_behavior == "Late":
    interpretation = (
        f"With late payment, the simulated monthly payment is "
        f"RM {monthly_payment:,.2f}. Paying less each month slows "
        f"the reduction of the outstanding balance. Compared with "
        f"the on-time scenario, the estimated additional repayment "
        f"cost is RM {difference:,.2f}."
    )

else:
    interpretation = (
        f"The on-time scenario uses the calculated monthly payment "
        f"of RM {monthly_payment:,.2f} as the baseline for comparison "
        f"with early and late payment strategies."
    )

if has_salary_input:
    interpretation += (
        f" Based on your monthly salary of RM {monthly_salary:,.2f}, this "
        f"payment represents about {dti_ratio:.1f}% of your income, which "
        f"is considered \"{get_affordability_status(dti_ratio)['label']}\" "
        f"under the general 30–35% guideline."
    )
else:
    interpretation += (
        " Add your monthly salary in the sidebar to see how this payment "
        "compares to your income."
    )

st.markdown(
    f"""
    <div class="insight-card">
        <div class="insight-title">Scenario Insight</div>
        <div class="insight-text">{interpretation}</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DETAILED PAYMENT SCHEDULE
# ============================================================

with st.expander("🔎 View Detailed Payment Schedule"):

    display_schedule = schedule.copy()

    for column in [
        "Payment",
        "Interest",
        "Principal",
        "Remaining Balance"
    ]:
        display_schedule[column] = display_schedule[column].round(2)

    st.dataframe(
        display_schedule,
        width="stretch",
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <div style="text-align:center; color:#9A9297; font-size:12px;">
        Data Visualisation Assignment · AQIL ANUAR · 24000198<br>Loan & Credit Card Payment Simulator
    </div>
    """,
    unsafe_allow_html=True
)
