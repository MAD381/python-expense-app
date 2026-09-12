# python-expense-app# Expense Claims Portal

A Python and Streamlit-based corporate expense tracking application that handles claim submissions, multi-level manager approvals, and finance payout workflows.

## How to Run It
1. Ensure you have Python installed, then install Streamlit and Pandas:
   ```bash
   pip install streamlit pandas
   streamlit run app.py
```markdown
## Decisions and Assumptions Made
* **Mock Database via Session State:** Utilized Streamlit's `st.session_state` to persistently store users and claims.
* **Realistic Dummy Data:** Seeded the application with employee accounts, roles, and custom team additions like Anaya Roy.

## AI Tools Used
* **Gemini:** Used as a coding collaborator to structure the Streamlit UI, build role-based routing, and manage session states.

## What I Would Do Next If I Had Another Week
* Integrate a persistent backend database like SQLite or PostgreSQL.
* Add a file uploader to handle image and PDF receipt attachments.
