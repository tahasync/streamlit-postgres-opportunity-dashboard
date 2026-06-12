"""Page 8: Deadline alerts showing closing soon and expired opportunities.

Displays opportunities closing within 7 days and already expired ones
with quick-action buttons for Admin users.
"""

from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Deadline Alerts", page_icon="⏰", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login, require_admin, get_role
from db import get_engine
from queries import get_deadline_alerts, get_expired_opportunities, update_opportunity
from utils import days_until_deadline

require_login()

engine = st.session_state.get("engine") or get_engine()
role = get_role()

st.markdown(
    "<h1 style='text-align: center;'>⏰ Deadline Alerts</h1>",
    unsafe_allow_html=True,
)
st.markdown(f"*Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
st.markdown("---")

st.markdown("### ⚠️ Closing Soon (Next 7 Days)")

with st.spinner("Loading closing soon..."):
    closing_soon = get_deadline_alerts(engine)

st.metric("Closing Soon", len(closing_soon))

if not closing_soon.empty:
    st.warning(f"⚠️ {len(closing_soon)} opportunities are closing within the next 7 days.")
    st.dataframe(closing_soon, use_container_width=True, hide_index=True)
else:
    st.success("✅ No opportunities closing within the next 7 days.")

st.markdown("---")
st.markdown("### 🚨 Expired Opportunities")

with st.spinner("Loading expired..."):
    expired = get_expired_opportunities(engine)

st.metric("Expired", len(expired))

if not expired.empty:
    st.error(f"🚨 {len(expired)} opportunities have passed their deadline.")
    st.dataframe(expired, use_container_width=True, hide_index=True)

    for _, row in expired.iterrows():
        days_overdue = days_until_deadline(row["application_deadline"])
        days_text = f"{abs(days_overdue)} days overdue" if days_overdue is not None else "Unknown"

        with st.expander(
            f"ID {row['opportunity_id']} — {row['company_name']} — "
            f"{row['job_title']} ({days_text})",
            expanded=False,
        ):
            st.dataframe(
                expired[expired["opportunity_id"] == row["opportunity_id"]],
                use_container_width=True,
                hide_index=True,
            )
            if role == "Admin":
                if st.button(
                    f"Mark ID {row['opportunity_id']} as Expired",
                    key=f"expire_{row['opportunity_id']}",
                ):
                    try:
                        update_opportunity(
                            engine, row["opportunity_id"], {"status": "Expired"}
                        )
                        st.success(
                            f"Opportunity ID {row['opportunity_id']} marked as Expired."
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update: {e}")
else:
    st.success("✅ No expired opportunities found.")


