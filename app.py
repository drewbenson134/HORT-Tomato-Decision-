"""HORT 2000 Tomato Decision Lab — classroom simulation, not agronomic advice."""
import csv
import io
import streamlit as st

st.set_page_config(page_title="Tomato Decision Lab | HORT 2000", page_icon="🍅", layout="wide")
GEMS = {
    "Alex Morgan · Grower": ("#278055", "https://gemini.google.com/gem/10Ru1BVom8p37xHWD502GtTkUXFPd9plC?usp=sharing", "Profitability, feasibility, labor and production risk"),
    "Casey Brooks · Produce Buyer": ("#286DB0", "https://gemini.google.com/gem/1eSuOvG5v-p1zQf_rcp7MbkAZwWvLx5mu?usp=sharing", "Marketability, delivery reliability, quality and compliance"),
    "Jordan Ellis · Environmental Advocate": ("#8050A0", "https://gemini.google.com/gem/1HqIw7ygpAdf5UZQJ1ec2EzvPbGoW_9ZH?usp=sharing", "Nontarget species, chemical exposure and resistance"),
    "Dr. Taylor Reed · Extension Specialist": ("#C1792E", "https://gemini.google.com/gem/1nvwxKxreYLeIsfeB1eoQXO4JkE8rnIYd?usp=sharing", "Pest identification, scouting data and evidence-based IPM"),
}
OPTIONS = {
    "Intensified scouting + targeted action": {"cost": 4000, "efficacy": 50, "environment": "Moderate; depends on choice and timing of intervention"},
    "Immediate broad-area application": {"cost": 6500, "efficacy": 70, "environment": "Potentially higher nontarget and resistance concerns"},
    "Scouting + primarily nonchemical measures": {"cost": 2500, "efficacy": 25, "environment": "May reduce chemical exposure but could be less effective under high pressure"},
}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "initial_locked" not in st.session_state:
    st.session_state.initial_locked = False
st.title("🍅 The $25,000 Tomato Decision")
st.caption("HORT 2000 • AI stakeholder negotiation and transparent economic decision-making")
st.warning("Educational scenario: all prices, losses, intervention costs and efficacies are illustrative assumptions, not field forecasts or pesticide recommendations.")
t1,t2,t3,t4 = st.tabs(["1 · Case & prediction", "2 · Decision simulator", "3 · Stakeholders", "4 · Defend & export"])
with t1:
    st.subheader("South Georgia tomato farm: whitefly pressure before harvest")
    st.write("A 10-acre fresh-market tomato crop is approximately 21 days from first harvest. Whitefly populations are increasing. The grower needs a plan that considers profitability, buyer requirements, environmental risks, and evidence-based integrated pest management (IPM).")
    a,b,c = st.columns(3)
    a.metric("Acres", "10")
    b.metric("Projected saleable yield", "30,000 lb/acre")
    c.metric("Assumed price", "$0.80/lb")
    st.write("**Your task:** Recommend an intervention, identify what additional scouting evidence you need, and defend the recommendation to four competing stakeholders.")
    st.radio("Initial prediction — before you consult a Gem", list(OPTIONS), key="initial_prediction", disabled=st.session_state.initial_locked)
    st.text_area("Why is this your initial choice?", key="initial_rationale", placeholder="Use horticultural reasoning; explain what is uncertain.", disabled=st.session_state.initial_locked)
    if not st.session_state.initial_locked:
        if st.button("Lock In My Initial Decision", type="primary"):
            rationale = st.session_state.initial_rationale.strip()
            if len(rationale) < 20:
                st.warning("Explain your reasoning in at least 20 characters before locking in your decision.")
            else:
                st.session_state.locked_initial_prediction = st.session_state.initial_prediction
                st.session_state.locked_initial_rationale = rationale
                st.session_state.initial_locked = True
                st.rerun()
        st.info("Record your prediction before exploring the simulator and stakeholder conversations.")
    else:
        st.success("Initial decision recorded. Investigate the economic consequences and consult the four stakeholders. You will revisit your original reasoning at the end.")
        st.caption("Your initial response is now locked for comparison with your final decision.")
with t2:
    st.subheader("Compare hypothetical management strategies")
    st.write("The economic model calculates revenue preserved minus intervention cost. Efficacy means the fraction of the **assumed loss** avoided—not the fraction of whiteflies killed.")
    left,right = st.columns([1,1])
    with left:
        acres = st.number_input("Production area (acres)", 1, 200, 10, 1)
        yield_lb = st.number_input("Marketable yield without new losses (lb/acre)", 1000, 100000, 30000, 1000)
        price = st.number_input("Farm-gate price ($/lb)", 0.1, 10.0, 0.8, 0.05, format="%.2f")
        loss_pct = st.slider("Potential revenue loss without intervention (%)", 0, 60, 20, 1)
        budget = st.number_input("Maximum new-management budget ($)", 0, 200000, 8000, 500)
    with right:
        strategy = st.selectbox("Inspect management strategy", list(OPTIONS))
        defaults = OPTIONS[strategy]
        cost = st.slider("Assumed management cost ($)", 0, 15000, defaults["cost"], 250, key=f"cost_{strategy}")
        efficacy = st.slider("Assumed proportion of losses prevented (%)", 0, 100, defaults["efficacy"], 5, key=f"eff_{strategy}")
        risk = defaults["environment"]
        st.caption(f"Qualitative environmental consideration: {risk}.")
    gross = acres * yield_lb * price
    threatened = gross * loss_pct / 100
    preserved = threatened * efficacy / 100
    net = preserved - cost
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Gross revenue at risk", f"${threatened:,.0f}")
    c2.metric("Revenue preserved", f"${preserved:,.0f}")
    c3.metric("Net economic benefit", f"${net:,.0f}")
    c4.metric("Within budget?", "Yes" if cost <= budget else "No")
    st.write("**Sensitivity test:** Change the potential loss or efficacy. Does your preferred strategy change? How confident are you in those assumptions?")
    st.caption("Formula: gross revenue = acres × yield × price; avoided loss = gross revenue × loss fraction × efficacy fraction; net benefit = avoided loss − intervention cost. Other costs and consequences are excluded.")
with t3:
    st.subheader("Consult the four Gems")
    st.write("Open each Gemini Gem in a new tab. Challenge the stakeholder with your preliminary plan. Gemini account access and the Gem owner's sharing permissions may be required.")
    for name,(color,url,concern) in GEMS.items():
        st.markdown(f"#### {name}")
        st.write(concern)
        st.link_button(f"Talk with {name.split(' · ')[0]}", url)
        st.divider()
    st.info("Ask: What would you object to? What evidence could change your position? What compromise would you accept?")
with t4:
    st.subheader("Negotiate, revise and defend")
    if st.session_state.initial_locked:
        st.markdown("**Your locked initial decision**")
        st.write(st.session_state.locked_initial_prediction)
        st.info(st.session_state.locked_initial_rationale)
    else:
        st.warning("Your initial decision has not been locked yet. Return to Tab 1 to record it before submitting your final recommendation.")
    st.radio("Final recommended strategy", list(OPTIONS), key="final_prediction")
    evidence = st.text_area("What biological or scouting evidence supports your decision?", key="evidence")
    stakeholders = st.text_area("How does your recommendation address all four stakeholders?", key="stakeholder_response")
    tradeoff = st.text_area("Which tradeoff remains unresolved? What would change your recommendation?", key="tradeoff")
    st.checkbox("I considered whether the scenario's efficacy and cost assumptions are credible", key="assumptions")
    if st.button("Review my reasoning", type="primary"):
        missing = []
        if len(evidence.strip()) < 45: missing.append("Add specific scouting and biological evidence, not just a treatment preference.")
        if len(stakeholders.strip()) < 65: missing.append("Explain how each of the four stakeholders is affected.")
        if len(tradeoff.strip()) < 35: missing.append("Identify an unresolved risk or a condition that would change your recommendation.")
        if not st.session_state.assumptions: missing.append("Evaluate uncertainty in modeled treatment efficacy and costs.")
        if missing:
            st.warning("Decision-review prompts (not an AI grade):")
            for item in missing: st.write("• " + item)
        else:
            st.success("Your response addresses the four review prompts. Now ask another group to challenge the scientific and economic assumptions.")
        st.session_state.submitted = True
    if st.session_state.initial_locked:
        st.markdown("**Initial versus final recommendation**")
        st.write(f"Initial: **{st.session_state.locked_initial_prediction}** → Final: **{st.session_state.final_prediction}**")
        if st.session_state.locked_initial_prediction == st.session_state.final_prediction:
            st.caption("The strategy remained the same. Explain how your reasoning became stronger or more nuanced.")
        else:
            st.caption("Your recommendation changed. Explain which new evidence or stakeholder concern drove the revision.")
    records = [
        ("Initial strategy",st.session_state.get("locked_initial_prediction", "NOT LOCKED")),
        ("Initial rationale",st.session_state.get("locked_initial_rationale", "NOT LOCKED")),
        ("Final strategy",st.session_state.get("final_prediction", "")),
        ("Scouting and biological evidence", evidence),
        ("Stakeholder considerations", stakeholders),
        ("Unresolved tradeoffs",tradeoff),
        ("Assumptions reviewed",str(st.session_state.assumptions)),
    ]
    buf=io.StringIO()
    writer=csv.writer(buf)
    writer.writerow(["Field","Response"])
    writer.writerows(records)
    st.download_button("Download my responses (CSV)", buf.getvalue(), file_name="tomato_decision_response.csv",mime="text/csv")
st.divider()
st.caption("Source background: UGA CAES Commercial Tomato Production Handbook (B1312; reviewed January 2017). Confirm current pest management guidance and product labels separately. https://fieldreport.caes.uga.edu/publications/B1312/commercial-tomato-production-handbook/")
