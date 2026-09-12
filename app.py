import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Expense Claims Portal", layout="wide")

# Initialize session state for users and claims if not already present
if 'users' not in st.session_state:
    st.session_state.users = [
        {"id": "u1", "name": "Rahul Sharma", "role": "staff", "limit": 5000},
        {"id": "u2", "name": "Priya Patel", "role": "staff", "limit": 5000},
        {"id": "m1", "name": "Amit Verma (Manager)", "role": "manager", "limit": 15000},
        {"id": "f1", "name": "Neha Gupta (Finance)", "role": "finance", "limit": 50000},
        {"id": "u3", "name": "Ananya Roy", "role": "staff", "limit": 5000},
        {"id": "m2", "name": "Vikram Singh (Manager)", "role": "manager", "limit": 15000},
    ]

if 'claims' not in st.session_state:
    st.session_state.claims = [
        {"id": "c1", "user_id": "u1", "user_name": "Rahul Sharma", "category": "Taxis", "amount": 250, "date": "2026-06-01", "text": "Auto ride to client office, 250 rs", "status": "Pending", "duplicate": False},
        {"id": "c2", "user_id": "u2", "user_name": "Priya Patel", "category": "Supplies", "amount": 650, "date": "2026-06-01", "text": "Printer ink and paper", "status": "Pending", "duplicate": True},
    ]

# Sidebar Role Switcher
st.sidebar.header("User Portal Simulation")
user_names = [u["name"] for u in st.session_state.users]
selected_user_name = st.sidebar.selectbox("Switch User View:", user_names)
current_user = next(u for u in st.session_state.users if u["name"] == selected_user_name)

st.sidebar.markdown(f"**Active Role:** `{current_user['role'].upper()}`")

st.title("🏢 Company Expense Claims Portal")

# --- 1. FILE A CLAIM (Staff & Managers) ---
st.header("File a New Claim")
with st.form("claim_form"):
    receipt_text = st.text_area("Paste Receipt Text / Screenshot Note:", placeholder="e.g., Auto ride 200 rs on 12th Oct")
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount (INR):", min_value=1.0, value=200.0)
    with col2:
        category = st.selectbox("Category", ["Taxis", "Travel", "Meals", "Supplies"])
    
    submitted = st.form_submit_button("AI Parse & Submit Claim")
    if submitted:
        # Check for duplicates
        is_dup = any(c['amount'] == amount and c['category'] == category for c in st.session_state.claims)
        
        new_claim = {
            "id": f"c_{datetime.now().timestamp()}",
            "user_id": current_user["id"],
            "user_name": current_user["name"],
            "category": category,
            "amount": amount,
            "date": str(datetime.now().date()),
            "text": receipt_text,
            "status": "Pending",
            "duplicate": is_dup
        }
        st.session_state.claims.insert(0, new_claim)
        if is_dup:
            st.warning("Claim submitted, but flagged as a potential duplicate receipt!")
        else:
            st.success("Claim successfully submitted!")

# --- 2. MANAGER APPROVAL PORTAL ---
if current_user["role"] == "manager":
    st.markdown("---")
    st.header("Manager Sign-Off Portal")
    st.info("Rule Check: Managers cannot approve their own claims.")
    
    for claim in st.session_state.claims:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            st.write(f"**{claim['user_name']}** ({claim['category']}) - ₹{claim['amount']}")
            st.caption(f"Note: {claim['text']}")
        with col2:
            st.write(f"Status: **{claim['status']}**")
        with col3:
            if st.button("Approve", key=f"app_{claim['id']}"):
                if claim['user_id'] == current_user['id']:
                    st.error("Error: You cannot approve your own claim!")
                else:
                    claim['status'] = "Approved"
                    st.rerun()
        with col4:
            if st.button("Reject", key=f"rej_{claim['id']}"):
                claim['status'] = "Rejected"
                st.rerun()

# --- 3. FINANCE PAYOUT & MONTHLY SUMMARY ---
if current_user["role"] == "finance":
    st.markdown("---")
    st.header("Finance Monthly Summary & Payouts")
    
    approved_claims = [c for c in st.session_state.claims if c['status'] in ['Approved', 'Paid']]
    total_spend = sum(c['amount'] for c in approved_claims)
    st.metric(label="Total Approved Monthly Spend", value=f"₹{total_spend}")
    
    for claim in st.session_state.claims:
        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.write(f"**{claim['user_name']}** - ₹{claim['amount']} ({claim['category']})")
            st.caption(f"Status: {claim['status']}")
        with col2:
            if claim['status'] == 'Paid':
                st.text("Locked (Paid)")
            else:
                if st.button("Mark as Paid", key=f"pay_{claim['id']}"):
                    claim['status'] = "Paid"
                    st.rerun()

# --- ALL CLAIMS HISTORY ---
st.markdown("---")
st.header("All Company Claims History")
for c in st.session_state.claims:
    st.write(f"- **{c['user_name']}** filed ₹{c['amount']} for *{c['category']}* [{c['status']}]")
    if c['duplicate']:
        st.caption("⚠️ Flagged as potential duplicate receipt.")