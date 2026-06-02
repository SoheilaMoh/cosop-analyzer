from io import BytesIO
import os
import re

import pandas as pd
import plotly.express as px
import streamlit as st

from src.pdf_processor import extract_pdf_text
from src.partner_finder import find_partner_mentions, summarize_partners
from src.llm_extractor import extract_partners_with_gpt
from src.validator import validate_partners, deduplicate_partners


st.set_page_config(
    page_title="COSOP Analyzer",
    layout="wide"
)

DEFAULT_PDF_PATH = "data/Cambodia_COSOP.pdf"
OUTPUT_DIR = "outputs"


# =====================
# BASIC HELPERS
# =====================

def make_safe_key(text):
    return re.sub(
        r"[^a-zA-Z0-9_]+",
        "_",
        str(text).lower()
    ).strip("_")


def dataframe_to_excel_bytes(df):
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    return output


def clean_gpt_results(raw_results):
    validated = validate_partners(raw_results)
    return deduplicate_partners(validated)


def get_cache_path(document_name):
    safe_name = make_safe_key(document_name)
    return os.path.join(
        OUTPUT_DIR,
        f"{safe_name}_gpt_partner_table.xlsx"
    )


def save_cached_results(df, cache_path):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_excel(
        cache_path,
        index=False,
        engine="openpyxl"
    )


def load_cached_results(cache_path):
    if os.path.exists(cache_path):
        return pd.read_excel(cache_path)
    return None


def save_uploaded_pdf(uploaded_file):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    safe_name = make_safe_key(uploaded_file.name)
    uploaded_path = os.path.join(
        OUTPUT_DIR,
        f"uploaded_{safe_name}.pdf"
    )

    with open(uploaded_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return uploaded_path


# =====================
# PDF INPUT
# =====================

st.title("COSOP Analyzer")

st.write(
    "Analyze COSOP PDF documents and extract IFAD partner information using GPT-based structured extraction."
)

uploaded_file = st.file_uploader(
    "Upload a COSOP PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    if not uploaded_file.name.lower().endswith(".pdf"):
        st.error("Invalid file type. Please upload a PDF file.")
        st.stop()

    pdf_path = save_uploaded_pdf(uploaded_file)
    document_name = uploaded_file.name

else:
    pdf_path = DEFAULT_PDF_PATH
    document_name = os.path.basename(DEFAULT_PDF_PATH)

cache_path = get_cache_path(document_name)

try:
    pages = extract_pdf_text(pdf_path)
except Exception as error:
    st.error(f"Failed to process PDF: {error}")
    st.stop()

if not pages:
    st.error("No text could be extracted from the PDF.")
    st.stop()

partner_mentions = find_partner_mentions(pages)
partner_summary = summarize_partners(partner_mentions)

st.success(
    f"PDF loaded successfully: {document_name} | Total pages: {len(pages)}"
)


# =====================
# DASHBOARD HELPERS
# =====================

def render_kpis(df):
    if df.empty:
        st.warning("No partner data available.")
        return

    col1, col2, col3, col4 = st.columns(4)

    total_partners = len(df)
    total_mentions = int(df["mention_count"].sum())
    key_partners = len(df[df["mention_count"] > 1])

    top_partner_row = (
        df.sort_values("mention_count", ascending=False)
        .iloc[0]
    )

    top_partner_name = top_partner_row["partner_name"]
    top_partner_mentions = int(top_partner_row["mention_count"])

    col1.metric("Total Partners", total_partners)
    col2.metric("Total Mentions", total_mentions)
    col3.metric("Key Partners", key_partners)
    col4.metric(
        "Top Partner",
        f"{top_partner_mentions} mentions",
        top_partner_name
    )


def render_top_partners_chart(df, title):
    chart_key = make_safe_key(title)

    top_partners = (
        df.sort_values("mention_count", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_partners,
        x="mention_count",
        y="partner_name",
        orientation="h",
        color="mention_count",
        color_continuous_scale="Tealgrn",
        template="plotly_white",
        title="Top 10 Partners by Mention Count"
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        height=520,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key=f"top_partners_chart_{chart_key}"
    )


def render_donut_chart(df, title):
    chart_key = make_safe_key(title)

    partner_type_counts = (
        df["partner_type"]
        .value_counts()
        .reset_index()
    )

    partner_type_counts.columns = ["Partner Type", "Count"]

    fig = px.pie(
        partner_type_counts,
        names="Partner Type",
        values="Count",
        hole=0.45,
        title="Partner Ecosystem Composition"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent"
    )

    fig.update_layout(
        showlegend=True,
        height=520,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key=f"donut_chart_{chart_key}"
    )


def render_partner_ranking_table(df):
    st.subheader("Partner Ranking Table")

    ranking_df = (
        df.sort_values("mention_count", ascending=False)
        .head(10)
        .copy()
        .reset_index(drop=True)
    )

    ranking_df.insert(
        0,
        "Rank",
        range(1, len(ranking_df) + 1)
    )

    st.dataframe(
        ranking_df[
            [
                "Rank",
                "partner_name",
                "partner_type",
                "mention_count",
                "pages"
            ]
        ],
        hide_index=True,
        width="stretch"
    )


def render_partner_profile_view(df, title):
    profile_key = make_safe_key(title)

    st.subheader("Partner Profile View")

    selected_partner = st.selectbox(
        "Select a partner to inspect",
        options=sorted(df["partner_name"].unique()),
        key=f"profile_{profile_key}"
    )

    partner_row = df[
        df["partner_name"] == selected_partner
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Mentions",
            int(partner_row["mention_count"])
        )

        st.write(
            f"**Partner Type:** {partner_row['partner_type']}"
        )

    with col2:
        st.write("**Pages**")
        st.write(partner_row["pages"])

    st.write("**Roles**")
    st.write(partner_row["roles"])

    st.write("**Sample Evidence**")
    st.info(partner_row["sample_evidence"])

    if "all_evidence" in df.columns:
        evidence_items = [
            item.strip()
            for item in str(partner_row["all_evidence"]).split(" || ")
            if item.strip()
        ]

        if evidence_items:
            with st.expander("Show all evidence sentences"):
                for i, evidence in enumerate(evidence_items, start=1):
                    st.write(f"**Evidence {i}:**")
                    st.info(evidence)


def render_master_table(df, title):
    table_key = make_safe_key(title)

    st.subheader("Partner Master Table")

    search_text = st.text_input(
        "Search partner name",
        key=f"search_{table_key}"
    )

    filtered_df = df.copy()

    if search_text:
        filtered_df = filtered_df[
            filtered_df["partner_name"]
            .str.contains(search_text, case=False, na=False)
        ]

    partner_type_options = ["All"] + sorted(
        filtered_df["partner_type"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_partner_type = st.selectbox(
        "Filter by partner type",
        options=partner_type_options,
        key=f"type_filter_{table_key}"
    )

    if selected_partner_type != "All":
        filtered_df = filtered_df[
            filtered_df["partner_type"] == selected_partner_type
        ]

    max_mentions = int(df["mention_count"].max())

    if max_mentions > 1:
        min_mentions = st.slider(
            "Minimum mention count",
            min_value=1,
            max_value=max_mentions,
            value=1,
            key=f"min_mentions_{table_key}"
        )
    else:
        min_mentions = 1
        st.caption(
            "All partners have a single mention. Mention filter disabled."
        )

    filtered_df = filtered_df[
        filtered_df["mention_count"] >= min_mentions
    ]

    st.dataframe(
        filtered_df,
        hide_index=True,
        width="stretch"
    )

    excel_output = dataframe_to_excel_bytes(filtered_df)

    st.download_button(
        label="Download Partner Table as Excel",
        data=excel_output,
        file_name="partner_table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"download_{table_key}"
    )




def render_dashboard(df, title="Partner Analytics Dashboard"):
    st.header(title)

    if df.empty:
        st.warning("No partner data available for dashboard.")
        return

    render_kpis(df)

    st.divider()

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        render_top_partners_chart(df, title)

    with chart_col2:
        render_donut_chart(df, title)

    st.divider()

    render_partner_ranking_table(df)

    st.divider()

    render_partner_profile_view(df, title)

    st.divider()

    render_master_table(df, title)


# =====================
# LOAD CACHED DASHBOARD
# =====================

cached_df = load_cached_results(cache_path)

if cached_df is not None:
    render_dashboard(
        cached_df,
        title="Partner Analytics Dashboard"
    )
else:
    st.warning(
        "No cached GPT results found for this PDF. Run full COSOP extraction once to generate the dashboard cache."
    )


# =====================
# GPT EXTRACTION TOOLS
# =====================

def run_gpt_on_pages(pages_to_process, label):
    all_results = []

    with st.spinner(f"Running GPT extraction on {label}..."):
        progress = st.progress(0)
        status = st.empty()

        total_pages = len(pages_to_process)

        for i, page in enumerate(pages_to_process):
            page_results = extract_partners_with_gpt(
                page["text"][:4000],
                page["page"]
            )

            all_results.extend(page_results)

            status.write(
                f"Processing page {i + 1}/{total_pages} "
                f"(COSOP page {page['page']}) | "
                f"Raw partners found: {len(all_results)}"
            )

            progress.progress((i + 1) / total_pages)

    return clean_gpt_results(all_results)


st.header("GPT Extraction Tools")

selected_page = st.selectbox(
    "Select a page to preview or analyze",
    options=[page["page"] for page in pages],
    key="selected_page"
)

page_text = next(
    page["text"] for page in pages if page["page"] == selected_page
)

col_a, col_b, col_c = st.columns(3)

with col_a:
    run_current_page = st.button(
        "Run GPT On Current Page",
        key="gpt_current_page"
    )

with col_b:
    run_first_10 = st.button(
        "Run GPT On First 10 Pages",
        key="gpt_first_10_pages"
    )

with col_c:
    run_entire_cosop = st.button(
        "Run GPT On Entire COSOP",
        key="gpt_entire_cosop"
    )


if run_current_page:
    raw_results = extract_partners_with_gpt(
        page_text[:4000],
        selected_page
    )

    final_results = clean_gpt_results(raw_results)

    if final_results:
        current_df = pd.DataFrame(final_results)

        render_dashboard(
            current_df,
            title=f"GPT Extraction Results - Page {selected_page}"
        )
    else:
        st.warning("No structured partners extracted from this page.")


if run_first_10:
    final_results = run_gpt_on_pages(
        pages[:10],
        "the first 10 pages"
    )

    if final_results:
        first_10_df = pd.DataFrame(final_results)

        st.success(
            f"Completed! Final partners found: {len(first_10_df)}"
        )

        render_dashboard(
            first_10_df,
            title="GPT Extraction Results - First 10 Pages"
        )
    else:
        st.warning("No structured partners extracted from the first 10 pages.")


if run_entire_cosop:
    final_results = run_gpt_on_pages(
        pages,
        "the full COSOP document"
    )

    if final_results:
        full_gpt_df = pd.DataFrame(final_results)

        save_cached_results(
            full_gpt_df,
            cache_path
        )

        st.success(
            f"Full COSOP extraction completed! Final partners found: {len(full_gpt_df)}"
        )

        render_dashboard(
            full_gpt_df,
            title="GPT Extraction Results - Entire COSOP"
        )
    else:
        st.warning("No structured partners extracted from the full COSOP.")


# =====================
# PDF PAGE PREVIEW
# =====================

with st.expander("PDF Page Preview"):

    st.subheader(
        f"Page {selected_page} Text Preview"
    )

    st.text_area(
        "Extracted text",
        page_text[:2000],
        height=350
    )


# =====================
# RULE-BASED RESULTS
# =====================

st.header("Validation & Rule-Based Comparison")

with st.expander("Show rule-based extraction results"):
    if partner_summary:
        rule_df = pd.DataFrame(partner_summary)

        partner_types = ["All"] + sorted(
            rule_df["partner_type"].unique().tolist()
        )

        selected_type = st.selectbox(
            "Filter by partner type",
            options=partner_types,
            key="rule_based_partner_type_filter"
        )

        if selected_type != "All":
            rule_df = rule_df[
                rule_df["partner_type"] == selected_type
            ]

        st.dataframe(
            rule_df,
            hide_index=True,
            width="stretch"
        )

        rule_output = dataframe_to_excel_bytes(rule_df)

        st.download_button(
            label="Download Rule-Based Partner Summary as Excel",
            data=rule_output,
            file_name="rule_based_partner_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_rule_based_partner_summary"
        )
    else:
        st.warning("No rule-based partners found.")