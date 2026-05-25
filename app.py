import streamlit as st
import pandas as pd
from types import SimpleNamespace
from src.staging.staging_pipeline import run_staging
from src.rag.rag_engine import run_iterative_rag
from src.rag.Vector_store import load_vector_store
from src.rag.Embeddings import import_embedding_llm


@st.cache_resource
def load_vs():
    embeddings = import_embedding_llm()
    return load_vector_store(embeddings)

st.set_page_config(layout="wide")
st.title("Clinical Guidelines Summary System")

user_query = st.text_area(
    "Enter a patient description...",
    height=150,
    placeholder="Describe patient in detail..."
)
vector_store = load_vs()

if st.button("Run Patient Classification"):
    if not user_query.strip():
        st.warning("Please enter a patient description...")
        st.stop()

    with st.spinner("Running classification..."):
        #classification = run_staging(user_query, vector_store)
        classification = {  # DO TESTU
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
            "USG": "Hypoechogenic nodule 8 mm, irregular margins",
            "Biopsy": "Fine-needle aspiration performed"
        }

    st.session_state["classification"] = classification


if "classification" in st.session_state:

    st.header("Patient Classification - UICC TNM 8 Staging System")
    cls = st.session_state["classification"]
    st.subheader("TNM Classification")

    col = st.columns([1, 2])
    with col[0]:
        age = st.number_input("Age", value=int(cls.get("age", 0)))

        T = st.selectbox(
            "T",
            ["TX","T1","T1a","T1b","T2","T3","T3a","T3b","T4a","T4b"],
            index=0 if not cls.get("T") else
            ["TX","T1","T1a","T1b","T2","T3","T3a","T3b","T4a","T4b"].index(cls.get("T"))
        )

        N = st.selectbox(
            "N",
            ["NX","N0","N0a","N0b","N1","N1a","N1b"],
            index=0 if not cls.get("N") else
            ["NX","N0","N0a","N0b","N1","N1a","N1b"].index(cls.get("N"))
        )

        M = st.selectbox(
            "M",
            ["MX","M0","M1"],
            index=0 if not cls.get("M") else
            ["MX","M0","M1"].index(cls.get("M"))
        )
        Stage = st.text_input("UICC Stage", value=cls.get("Stage", ""))


    st.subheader("Cancer Type")
    col1, col2 = st.columns(2)

    with col1:
        label_input = st.text_input(
            "Label",
            value=cls["cancer_type"]["label"],
            help="Please write a particular type of cancer, for example Papillary Thyroid Carcinoma."
        )

    with col2:
        group_input = st.selectbox(
            "Group",
            [
                "Differentiated thyroid carcinoma",
                "Medullary thyroid carcinoma",
                "Anaplastic thyroid carcinoma"
            ],
            index=[
                "Differentiated thyroid carcinoma",
                "Medullary thyroid carcinoma",
                "Anaplastic thyroid carcinoma"
            ].index(cls["cancer_type"]["group"])
        )


    st.subheader("Diagnostics")
    col3, col4, col5 = st.columns(3)

    with col3:
        bethesda = st.text_area(
            "Bethesda System Category",
            value=cls.get("Bethesda_System_Category", ""),
            height=120,
            help="Information about Bethesda System category."
        )

    with col4:
        usg = st.text_area(
            "USG (ultrasound)",
            value=cls.get("USG", ""),
            height=120,
            help="Was USG performed? Write information about USG."
        )

    with col5:
        biopsy = st.text_area(
            "Biopsy/FNA",
            value=cls.get("Biopsy", ""),
            height=120,
            help="Was biopsy performed? Write information about biopsy."
        )

    edited_classification = {
        "age": age,
        "T": T,
        "N": N,
        "M": M,
        "cancer_type": {
            "label": label_input,
            "group": group_input
        },
        "Stage": Stage,
        "Bethesda_System_Category": bethesda,
        "USG": usg,
        "Biopsy": biopsy,
    }
    st.session_state["classification"] = edited_classification

    if "classification" in st.session_state:
        if st.button("Generate Guidelines"):
            st.header("Guidelines by Organization")
            with st.spinner("Generating guidelines..."):
                #guidelines = run_iterative_rag(vector_store, st.session_state["classification"], debug=False)
                guidelines = { #DO TESTU
                    "answers": {
                        "KOM": SimpleNamespace(
                            recommended=["rec1_KOM", "rec2_KOM", "rec3_KOM"],
                            to_consider=["con1_KOM", "con2_KOM", "con3_KOM"],
                            not_recommended=["not1_KOM", "not2_KOM", "not3_KOM"]
                        ),
                        "NCCN": SimpleNamespace(
                            recommended=["rec1_NCCN", "rec2_NCCN", "rec3_NCCN"],
                            to_consider=["con1_NCCN", "con2_NCCN", "con3_NCCN"],
                            not_recommended=["not1_NCCN", "not2_NCCN", "not3_NCCN"]
                        ),
                        "ATA": SimpleNamespace(
                            recommended=["rec1_ATA", "rec2_ATA", "rec3_ATA", "rec"],
                            to_consider=["con1_ATA", "con2_ATA", "con3_ATA"],
                            not_recommended=["not1_ATA", "not2_ATA", "not3_ATA", "not3_ESMO", "not3_ESMO", "not3_ESMO"]
                        ),
                        "BTA": SimpleNamespace(
                            recommended=["rec1_BTA", "rec2_BTA", "rec3_BTA"],
                            to_consider=["con1_BTA", "con2_BTA", "con3_BTA"],
                            not_recommended=["not1_BTA", "not2_BTA", "not3_BTA", "not3_ESMO"]
                        ),
                        "ESMO": SimpleNamespace(
                            recommended=["rec1_ESMO", "rec2_ESMO", "rec3_ESMO"],
                            to_consider=["con1_ESMO", "con2_ESMO", "con3_ESMO"],
                            not_recommended=["not1_ESMO", "not2_ESMO", "not3_ESMO", "not3_ESMO", "not3_ESMO"]
                        ),
                    },
                    "metrics": {}
                }

            if not guidelines:
                st.error("No guidelines generated")
                st.stop()

            answers = guidelines.get("answers", {})
            metrics = guidelines.get("metrics", {})
            orgs = list(answers.keys())

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
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.header("Guidelines by Organization")
            cols = st.columns(len(answers))
            for col, org in zip(cols, answers.keys()):
                with col:
                    st.markdown(f"## {org}")


            st.subheader("🟢 Recommended")
            max_len = max(len(answers[o].recommended) for o in orgs)

            rec_data = {
                org: answers[org].recommended + [""] * (max_len - len(answers[org].recommended))
                for org in orgs
            }
            df_rec = pd.DataFrame(rec_data)
            html = df_rec.to_html(index=False, header=False, escape=False)
            st.markdown(
                f"""
                <style>
                table {{
                    width: 100%;
                    table-layout: fixed;
                    border-collapse: collapse;
                }}

                td {{
                    width: {100 / len(df_rec.columns)}%;
                    padding: 8px;
                    border: 1px solid #333;
                    word-wrap: break-word;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(html, unsafe_allow_html=True)



            st.subheader("🟡 To Consider")
            max_len = max(len(answers[o].to_consider) for o in orgs)

            con_data = {
                org: answers[org].to_consider + [""] * (max_len - len(answers[org].to_consider))
                for org in orgs
            }
            df_con = pd.DataFrame(con_data)
            html = df_con.to_html(index=False, header=False, escape=False)
            st.markdown(html, unsafe_allow_html=True)



            st.subheader("🔴 Not Recommended")
            max_len = max(len(answers[o].not_recommended) for o in orgs)

            not_data = {
                org: answers[org].not_recommended + [""] * (max_len - len(answers[org].not_recommended))
                for org in orgs
            }
            df_not = pd.DataFrame(not_data)
            html = df_not.to_html(index=False, header=False, escape=False)
            st.markdown(html, unsafe_allow_html=True)

