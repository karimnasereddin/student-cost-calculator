import streamlit as st

st.set_page_config(page_title="Budget Coach", page_icon="💬", layout="centered")
st.title("💬 Budget Coach")
st.caption("Ask questions about your budget and get recommendations based on your results.")

# Make sure they visited the main page first
if "df" not in st.session_state:
    st.warning("Go to the main calculator page first so I can use your results.")
    st.stop()

df = st.session_state["df"]
monthly = st.session_state["monthly"]
yearly_income = st.session_state["yearly_income"]
total_yearly = st.session_state["total_yearly"]
hourly_wage = st.session_state["hourly_wage"]

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hey! Ask me things like: 'Where can I cut costs?' or 'How many hours do I need to work?'"}
    ]

def coach_reply(user_text: str) -> str:
    user_text = user_text.lower()

    # Compute some insights
    top_row = df.loc[df["Yearly Cost"].idxmax()]
    top_cat = top_row["Category"]
    top_val = float(top_row["Yearly Cost"])
    top_pct = (top_val / total_yearly) * 100 if total_yearly > 0 else 0

    # Quick “what-if”
    save_40_mo = 40 * 12
    save_hours = (save_40_mo / hourly_wage) if hourly_wage > 0 else None

    # Simple intent rules (feels like an AI coach)
    if "cut" in user_text or "save" in user_text or "reduce" in user_text:
        suggestions = []
        # suggest based on biggest categories
        if top_cat.lower() == "housing":
            suggestions.append("Housing is your biggest lever. If possible: split rent, choose a cheaper plan, or sublet for summer terms.")
        if "entertain" in df["Category"].str.lower().tolist():
            suggestions.append("Try a cap: set Entertainment to a fixed monthly budget and track it weekly.")
        suggestions.append(f"Biggest cost is **{top_cat}** at **{top_pct:.0f}%** of your budget (${top_val:,.0f}/year).")
        suggestions.append(f"Quick win: cutting **$40/month** saves **${save_40_mo:,.0f}/year**" + (f" (~{save_hours:.1f} work hours)." if save_hours is not None else "."))
        return "\n\n".join(suggestions)

    if "hours" in user_text or "work" in user_text or "job" in user_text:
        weekly_cost = total_yearly / 52
        hours_needed_week = (weekly_cost / hourly_wage) if hourly_wage > 0 else 0
        return (
            f"Your total is **${total_yearly:,.0f}/year** (~**${weekly_cost:,.0f}/week**).\n\n"
            f"At **${hourly_wage:.2f}/hr**, you need about **{hours_needed_week:.1f} hrs/week** to break even."
        )

    if "income" in user_text or "short" in user_text or "gap" in user_text:
        gap = yearly_income - total_yearly
        if gap >= 0:
            return f"You're projected to be **+${gap:,.0f}/year** ahead. Nice — consider putting the surplus into savings or investing."
        return f"You're projected to be **-${abs(gap):,.0f}/year** short. Best moves: reduce your top category or increase work hours slightly."

    if "biggest" in user_text or "where" in user_text:
        return f"Your biggest category is **{top_cat}** at **{top_pct:.0f}%** of your total (${top_val:,.0f}/year)."

    # Default helpful response
    return (
        "Try asking:\n"
        "- “Where can I cut costs?”\n"
        "- “How many hours do I need to work?”\n"
        "- “What’s my biggest expense?”\n"
        "- “Am I short or ahead?”"
    )

# Render chat
for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Input
user_prompt = st.chat_input("Ask about your budget...")
if user_prompt:
    st.session_state["messages"].append({"role": "user", "content": user_prompt})
    reply = coach_reply(user_prompt)
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.rerun()