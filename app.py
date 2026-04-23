import os
import streamlit as st
import clipboard

from graph import build_graph
from graph.state import PostState

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
METAPHOR_API_KEY = os.getenv("METAPHOR_API_KEY")

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI LinkedIn Post Generator",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

        .stApp { background-color: #0E1117; color: #E0E0E0; }
        .main { padding: 2rem; font-family: 'Inter', sans-serif; color: #E0E0E0; }

        .stExpander {
            background: rgba(17,17,17,0.7); border-radius: 15px; padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .stTextInput > div > div > input {
            background: rgba(17,17,17,0.7) !important; border-radius: 10px;
            border: 2px solid rgba(255,255,255,0.1);
            padding: 10px 15px; font-size: 16px; color: #E0E0E0;
        }

        .stSelectbox > div > div {
            background: rgba(17,17,17,0.7) !important; border-radius: 10px;
            border: 2px solid rgba(255,255,255,0.1);
        }

        div.stButton > button:first-child {
            background: linear-gradient(45deg, #0077B5, #00A0DC);
            color: white; padding: 12px 24px; border-radius: 10px;
            font-weight: 600; font-size: 16px; border: none;
            box-shadow: 0 4px 6px rgba(0,123,255,0.2); transition: all 0.3s ease;
        }

        .post-preview {
            background: rgba(17,17,17,0.7); padding: 25px; border-radius: 15px;
            border-left: 5px solid #0077B5; margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3); color: #E0E0E0;
        }

        h1, h2, h3 { color: #E0E0E0; font-family: 'Inter', sans-serif; font-weight: 600; }

        .success-message {
            padding: 15px; border-radius: 10px;
            background-color: rgba(40,167,69,0.2);
            border-left: 5px solid #28a745; margin: 10px 0; color: #E0E0E0;
        }

        .dark-card {
            background: rgba(17,17,17,0.7); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px; padding: 20px; color: #E0E0E0;
        }

        .gradient-header {
            background: linear-gradient(45deg, rgba(0,119,181,0.8), rgba(0,160,220,0.8));
            backdrop-filter: blur(10px);
        }

        header { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class='gradient-header' style='padding:20px;border-radius:15px;margin-bottom:30px;'>
        <h1 style='color:#E0E0E0;text-align:center;font-family:Inter,sans-serif;'>
            🤖 AI LinkedIn Post Generator
        </h1>
        <p style='color:#E0E0E0;text-align:center;font-size:18px;'>
            Multi-stage LangGraph pipeline — research → draft → evaluate → refine → publish
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

if "final_state" not in st.session_state:
    st.session_state.final_state = None

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

with st.expander("💡 Pro Tips for Better Results", expanded=True):
    st.markdown(
        """
        <div class='dark-card'>
            <h4 style='color:#00A0DC;'>Follow these guidelines:</h4>
            <ul style='list-style-type:none;padding-left:0;color:#E0E0E0;'>
                <li>✨ Use specific keywords related to your topic</li>
                <li>🎯 Choose a post type that aligns with your message</li>
                <li>🌍 Select appropriate language and length for your audience</li>
                <li>⚡ The pipeline generates 3 drafts, evaluates &amp; auto-refines the best one</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_blog_keywords = st.text_input(
        "🔑 **Enter main keywords for your post**",
        placeholder="e.g., Marketing Trends, Leadership Tips...",
        help="Use relevant keywords that define the topic of your LinkedIn post.",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        input_linkedin_type = st.selectbox(
            "📝 **Post Type**",
            (
                "General", "How to implements/build", "How-to Guides", "Polls",
                "Listicles", "Reality Check Posts", "Job Posts", "FAQs",
                "Checklists/Cheat Sheets",
            ),
            index=0,
            help="Choose the format that suits the message you want to deliver.",
        )
    with col2:
        input_linkedin_length = st.selectbox(
            "📏 **Post Length**",
            ("Short Form (300-500 words)", "Standard 1000 words", "Long Form (1500-2000 words)"),
            index=0,
            help="Decide the length of your post based on its complexity and target audience.",
        )
    with col3:
        input_linkedin_language = st.selectbox(
            "🌐 **Choose Language**",
            ("English", "Vietnamese", "Chinese", "Hindi", "Spanish"),
            index=0,
            help="Pick the language that resonates best with your audience.",
        )

# ---------------------------------------------------------------------------
# Generation pipeline
# ---------------------------------------------------------------------------

PIPELINE_STEPS = [
    ("🔍", "Researching topic with Exa search"),
    ("👥", "Profiling target audience"),
    ("📋", "Building post outline"),
    ("✍️", "Writing 3 parallel draft variants"),
    ("⚖️", "Evaluating drafts with 6-dimension rubric"),
    ("🏆", "Selecting highest-scoring draft"),
    ("🔧", "Refining selected draft"),
    ("📊", "Re-evaluating refined draft"),
    ("#️⃣", "Optimising hashtags"),
    ("✨", "Final LinkedIn formatting"),
]


def _run_pipeline(keywords, post_type, length, language):
    initial_state: PostState = {
        "keywords": keywords,
        "post_type": post_type,
        "length": length,
        "language": language,
        "raw_search_results": [],
        "summarized_research": "",
        "audience_profile": "",
        "outline": "",
        "drafts": [],
        "current_draft": "",
        "evaluation_scores": {},
        "critique": "",
        "iteration_count": 0,
        "final_post": "",
    }

    # Show all planned steps before starting
    step_md = "\n".join(f"{emoji} {label}" for emoji, label in PIPELINE_STEPS)
    st.info(f"**Pipeline steps:**\n{step_md}")

    graph = build_graph()
    with st.spinner("🤖 Running LangGraph pipeline (this may take ~60–90 seconds)…"):
        final_state = graph.invoke(initial_state)
    return final_state


if st.button("🚀 **Generate LinkedIn Post**"):
    if not input_blog_keywords:
        st.error("🚫 **Please provide keywords to generate a LinkedIn post!**")
    else:
        final_state = _run_pipeline(
            input_blog_keywords,
            input_linkedin_type,
            input_linkedin_length,
            input_linkedin_language,
        )
        st.session_state.final_state = final_state

# ---------------------------------------------------------------------------
# Results display
# ---------------------------------------------------------------------------

if st.session_state.final_state:
    state: PostState = st.session_state.final_state

    # ---- Final post ----
    st.markdown(
        "<div class='post-preview'><h3 style='color:#0077B5;'>📄 LinkedIn Post Preview</h3></div>",
        unsafe_allow_html=True,
    )
    st.write(state.get("final_post", ""))

    # ---- Action buttons ----
    col1, col2, _pad = st.columns([1, 1, 2])
    with col1:
        if st.button("📋 Copy to Clipboard", key="copy"):
            clipboard.copy(state.get("final_post", ""))
            st.markdown(
                "<div class='success-message'>✅ Copied to clipboard!</div>",
                unsafe_allow_html=True,
            )
    with col2:
        st.download_button(
            label="💾 Download Post",
            data=state.get("final_post", ""),
            file_name="linkedin_post.txt",
            mime="text/plain",
            key="download_post",
        )

    st.markdown("---")

    # ---- Evaluation Scorecard ----
    scores = state.get("evaluation_scores", {})
    # Prefer re-evaluated refined scores; fall back to best numbered draft
    display_scores = scores.get("refined") or {}
    if not display_scores:
        int_score_keys = [k for k in scores if isinstance(k, int) and k in scores]
        if int_score_keys:
            best_i = max(
                int_score_keys,
                key=lambda i: float(scores[i].get("total", 0)),
            )
            display_scores = scores[best_i]

    if display_scores:
        st.markdown("### 📊 Quality Scorecard")
        dims = [
            ("hook_strength", "Hook Strength"),
            ("engagement_potential", "Engagement Potential"),
            ("linkedin_algorithm_score", "LinkedIn Algorithm"),
            ("eeat_score", "E-E-A-T"),
            ("readability", "Readability"),
            ("cta_quality", "CTA Quality"),
        ]
        score_cols = st.columns(len(dims))
        for col, (key, label) in zip(score_cols, dims):
            val = float(display_scores.get(key, 0))
            color = "#28a745" if val >= 8 else "#ffc107" if val >= 5 else "#dc3545"
            col.markdown(
                f"""
                <div style='text-align:center;padding:10px;background:rgba(17,17,17,0.7);
                     border-radius:10px;border:1px solid rgba(255,255,255,0.1);'>
                    <div style='font-size:28px;font-weight:700;color:{color};'>{val:.0f}</div>
                    <div style='font-size:12px;color:#aaa;'>{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        total = float(display_scores.get("total", 0))
        st.markdown(
            f"<p style='text-align:center;margin-top:10px;color:#E0E0E0;'>"
            f"<strong>Total: {total:.0f} / 60</strong></p>",
            unsafe_allow_html=True,
        )

    # ---- Explain Choices ----
    with st.expander("🧠 Explain Choices", expanded=False):
        st.markdown("#### Why this draft was selected")
        int_keys = sorted(k for k in scores if isinstance(k, int))
        if int_keys:
            import pandas as pd

            style_labels = {0: "Story-driven", 1: "Data-driven", 2: "Contrarian"}
            rows = []
            for k in int_keys:
                s = scores[k]
                rows.append(
                    {
                        "Draft": style_labels.get(k, f"Draft {k + 1}"),
                        "Total": s.get("total", 0),
                        "Hook": s.get("hook_strength", 0),
                        "Engagement": s.get("engagement_potential", 0),
                        "Algorithm": s.get("linkedin_algorithm_score", 0),
                        "E-E-A-T": s.get("eeat_score", 0),
                        "Readability": s.get("readability", 0),
                        "CTA": s.get("cta_quality", 0),
                    }
                )
            st.dataframe(pd.DataFrame(rows).set_index("Draft"), use_container_width=True)

        critique = state.get("critique", "")
        if critique:
            st.markdown(f"**Critique applied during refinement:** {critique}")

        iters = state.get("iteration_count", 0)
        st.markdown(f"**Refinement iterations performed:** {iters}")

    # ---- Draft Comparison ----
    with st.expander("📝 View All 3 Draft Variants", expanded=False):
        drafts = state.get("drafts", [])
        style_labels = ["Story-driven ✍️", "Data-driven 📊", "Contrarian 🔥"]
        if drafts:
            tabs = st.tabs(style_labels[: len(drafts)])
            for tab, draft in zip(tabs, drafts):
                with tab:
                    st.write(draft)
        else:
            st.info("No draft variants available.")

    # ---- Re-Refine ----
    st.markdown("---")
    st.markdown("### 🔄 Re-Refine with Additional Instructions")
    extra_instructions = st.text_area(
        "Optional: add specific instructions for the next refinement pass",
        placeholder=(
            "e.g., Make the hook more provocative. Add a personal story. Shorten to 300 words."
        ),
        height=80,
    )
    if st.button("🔧 Re-Refine Post", key="rerefine"):
        from graph.nodes.refiner import refiner_node
        from graph.nodes.hashtags import hashtag_optimizer_node
        from graph.nodes.formatter import formatter_node

        current = dict(st.session_state.final_state)
        if extra_instructions:
            existing_critique = current.get("critique", "")
            separator = "\n\n" if existing_critique else ""
            current["critique"] = (
                existing_critique + separator + f"Additional instructions: {extra_instructions}"
            )
        with st.spinner("🔧 Refining…"):
            current = refiner_node(current)
            current = hashtag_optimizer_node(current)
            current = formatter_node(current)
        st.session_state.final_state = current
        st.rerun()
