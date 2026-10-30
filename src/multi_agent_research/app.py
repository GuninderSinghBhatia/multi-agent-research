import re
import sys

import streamlit as st

from multi_agent_research.pipeline import run_research_pipeline

# The pipeline prints scraped web text; stop Windows consoles crashing on unusual characters.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

st.set_page_config(page_title="Multi-Agent Research", page_icon="🔎", layout="wide")

st.title("🔎 Multi-Agent Research")
st.caption(
    "Search agent finds sources → Reader agent scrapes the best one → "
    "Writer drafts a report → Critic reviews it."
)

with st.form("research"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Latest advances in solid-state batteries",
    )
    submitted = st.form_submit_button("Run research", type="primary")

if submitted:
    topic = topic.strip()
    if not topic:
        st.warning("Enter a topic first.")
    else:
        with st.status("Starting research...", expanded=True) as status:
            def on_step(n, label):
                status.update(label=f"Step {n}/4: {label}...")
                st.write(f"**Step {n}/4:** {label}")

            try:
                st.session_state.result = run_research_pipeline(topic, on_step=on_step)
                st.session_state.topic = topic
                status.update(label="Research complete", state="complete", expanded=False)
            except Exception as e:
                status.update(label="Research failed", state="error")
                st.exception(e)

result = st.session_state.get("result")
if result:
    st.subheader(st.session_state.topic)

    match = re.search(r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", result["feedback"])
    if match:
        st.metric("Critic score", f"{match.group(1)}/10")

    report_tab, critic_tab, search_tab, scraped_tab = st.tabs(
        ["📄 Report", "🧐 Critic feedback", "🌐 Search results", "📖 Scraped content"]
    )

    with report_tab:
        st.markdown(result["report"])
        st.download_button(
            "Download report (.md)",
            data=result["report"],
            file_name=f"{st.session_state.topic[:50]}.md",
            mime="text/markdown",
        )

    with critic_tab:
        st.markdown(result["feedback"])

    with search_tab:
        st.markdown(result["search_results"])

    with scraped_tab:
        st.markdown(result["scraped_content"])
