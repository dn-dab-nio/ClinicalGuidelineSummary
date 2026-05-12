import streamlit as st
import pandas as pd
from src.staging.staging_pipeline import run_staging
from src.rag.rag_engine import run_iterative_rag
from src.rag.Vector_store import load_vector_store
from src.rag.Embeddings import import_embedding_llm


@st.cache_resource
def load_vs():
    embeddings = import_embedding_llm()
    return load_vector_store(embeddings)

st.set_page_config(layout="wide")
st.title('Clinical Guidelines Summary System')

user_query = st.text_input("Enter a patient description...")


###
if  st.button("Run Patient Classification"):
    if not user_query.strip():
        st.warning("Please enter a patient description...")
        st.stop()

    vector_store = load_vs()
    st.header("Patient Classification (TNM + UICC)")

    with st.spinner("Running classification..."):
        # classification = run_staging(user_query, vector_store)
        classification = { #DO TESTU
            "age": 45,
            "T": "T2",
            "N": "N1",
            "M": "M0",
            "cancer_type": {
                "label": "Papillary Thyroid Carcinoma",
                "group": "Differentiated thyroid carcinoma"
            },
            "Stage": "Stage II",
            "Bethesda_System_Category": "III (AUS)",
            "USG": "Performed; hypoechogenic nodule 8 mm, irregular margins, suspected microcalcifications, no lymph node involvement",
            "Biopsy": "Performed; fine‑needle aspiration"
        }

    st.session_state["classification"] = classification

if "classification" in st.session_state:
    st.header("Edit Patient Classification")
    cls = st.session_state["classification"]
    age =st.number_input("Age", value=int(cls.get("age", 0)))
    T = st.selectbox("T", ["TX", "T1", "T1a", "T1b", "T2", "T3", "T3a", "T3b", "T4a", "T4b"], index=0 if not cls.get("T") else ["TX", "T1", "T1a", "T1b", "T2", "T3", "T3a", "T3b", "T4a", "T4b"].index(cls.get("T")))
    N = st.selectbox("N", ["NX", "N0", "N0a", "N0b", "N1", "N1a", "N1b"], index=0 if not cls.get("N") else ["NX", "N0", "N0a", "N0b", "N1", "N1a", "N1b"].index(cls.get("N")))
    M = st.selectbox("M", ["MX", "M0", "M1"], index=0 if not cls.get("M") else ["MX", "M0", "M1"].index(cls.get("M")))
    Stage = st.text_input("UICC Stage", value=cls.get("Stage", ""))

    cancer = cls.get("cancer_type", {})
    label = cancer.get("label", "")
    group = cancer.get("group", "")

    st.subheader("Cancer Type")

    col1, col2 = st.columns(2)
    with col1:
        label_input = st.text_input("Label", value=label, help= "e.g. Papillary thyroid carcinoma")

    with col2:
        group_input = st.selectbox("Group", ["Differentiated thyroid carcinoma", "Medullary thyroid carcinoma", "Anaplastic thyroid carcinoma"],
                                    index=0 if not group else ["Differentiated thyroid carcinoma", "Medullary thyroid carcinoma", "Anaplastic thyroid carcinoma"].index(group))

    st.subheader("Diagnostics")
    col3, col4, col5 = st.columns(3)

    with col3:
        bethesda = st.text_input("Bethesda System Category", value="", help= cls.get("Bethesda_System_Category", ""))

    with col4:
        usg = st.text_input("USG (ultrasound)", value="", help= cls.get("USG", ""))

    with col5:
        biopsy = st.text_input("Biopsy/FNA", value="", help= cls.get("Biopsy", ""))

    edited_classification = {
        "age": age,
        "T": T,
        "N": N,
        "M": M,
        "cancer_type": {
                "label": label_input,
                "group": group_input
            },
        "stage": Stage,
        "Bethesda_System_Category": bethesda,
        "USG": usg,
        "Biopsy": biopsy,
    }

    st.session_state["edited_classification"] = edited_classification

    if "edited_classification" in st.session_state:
        if st.button("Generate Guidelines"):
            st.header("Guidelines by Organization")
            with st.spinner("Generating guidelines..."):
                guidelines = run_iterative_rag(vector_store, classification, debug=False)

            if not guidelines:
                st.error("No guidelines generated")
                st.stop()

            answers = guidelines.get("answers", {})
            metrics = guidelines.get("metrics", {})

            #SUMMARY
            rows = []
            for org, data in answers.items():
                rows.append({
                    "Organization": org,
                    "Recommended": len(data.recommended),
                    "To Consider": len(data.to_consider),
                    "Not Recommended": len(data.not_recommended),
                    "Iterations": metrics.get(org, {}).get("iterations_used", "N/A"),
                    "Status": metrics.get(org, {}).get("final_status", "N/A")
                })

            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)


            #GUIDELINES
            st.subheader("Detailed Guidelines")

            cols = st.columns(len(answers))
            for col, (org, data) in zip(cols, answers.items()):
                with col:
                    st.markdown(f"## {org}")

                    st.markdown("### 🟢 Recommended")
                    if data.recommended:
                        for item in data.recommended:
                            st.markdown(f"- {item}")
                    else:
                        st.write("No data")


                    st.markdown("### 🟡 To Consider")
                    if data.to_consider:
                        for item in data.to_consider:
                            st.markdown(f"- {item}")
                    else:
                        st.write("No data")

                    st.markdown("### 🔴 Not Recommended")
                    if data.not_recommended:
                        for item in data.not_recommended:
                            st.markdown(f"- {item}")
                    else:
                        st.write("No data")


                    st.markdown("---")
                    st.markdown("**Metrics**")
                    st.write(f"Iterations: {metrics.get(org, {}).get('iterations_used', 'N/A')}")
                    st.write(f"Status: {metrics.get(org, {}).get('final_status', 'N/A')}")
                    st.write(f"Contexts used: {metrics.get(org, {}).get('contexts_used', 'N/A')}")

            with st.expander("Debug metrics"):
                st.json(metrics)













#########
# if st.button("Generate summary"):
#     if not user_query.strip():
#         st.warning("Please enter a patient description...")
#         st.stop()
#
#     vector_store = load_vs()
#     st.header("Patient Classification (TNM + UICC)")
#     with st.spinner("Running classification..."):
#         classification = run_staging(user_query, vector_store)
#     df_class = pd.DataFrame(
#         [(k, str(v)) for k, v in classification.items()],
#         columns=["Field", "Value"]
#     )
#     st.table(df_class)
#
#     st.header("Guidelines by Organization")
#     with st.spinner("Generating guidelines..."):
#         guidelines = run_iterative_rag(vector_store, classification, debug=False)
#
#     if not guidelines:
#         st.error("No guidelines generated")
#         st.stop()
#
#     answers = guidelines.get("answers", {})
#     metrics = guidelines.get("metrics", {})
#
#     rows = []
#
#     for org, data in answers.items():
#         rows.append({
#             "Organization": org,
#             "Recommended": "✔" if data.recommended else "—",
#             "To Consider": "✔" if data.to_consider else "—",
#             "Not Recommended": "✔" if data.not_recommended else "—",
#             "Iterations": metrics.get(org, {}).get("iterations_used", "N/A"),
#             "Status": metrics.get(org, {}).get("final_status", "N/A")
#         })
#
#     df_guidelines = pd.DataFrame(rows)
#     st.table(df_guidelines)
#
#
#     def format_text(text: str):
#         if not text:
#             return ["No information available"]
#
#         # rozbij po kropkach (prosty NLP hack)
#         sentences = [s.strip() for s in text.split(".") if s.strip()]
#
#         return sentences
#
#
#     st.subheader("Detailed Guidelines")
#
#     cols = st.columns(len(answers))
#
#     for col, (org, data) in zip(cols, answers.items()):
#         with col:
#             st.markdown(f"## {org}")
#
#             st.markdown("### 🟢 Recommended")
#             rec_list = format_text(data.recommended)
#
#             for r in rec_list[:5]:
#                 st.markdown(f"- {r}")
#
#             st.markdown("### 🟡 To Consider")
#             consider_list = format_text(data.to_consider)
#
#             for c in consider_list[:5]:
#                 st.markdown(f"- {c}")
#
#             st.markdown("### 🔴 Not Recommended")
#             not_rec_list = format_text(data.not_recommended)
#
#             for n in not_rec_list[:5]:
#                 st.markdown(f"- {n}")
#
#             st.markdown("---")
#             st.markdown("**Metrics**")
#             st.write(f"Iterations: {metrics.get(org, {}).get('iterations_used', 'N/A')}")
#             st.write(f"Status: {metrics.get(org, {}).get('final_status', 'N/A')}")
#             st.write(f"Contexts used: {metrics.get(org, {}).get('contexts_used', 'N/A')}")
#
#     with st.expander("Debug metrics"):
#         st.json(metrics)
#
