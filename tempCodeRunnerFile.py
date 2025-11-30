import streamlit as st
from analyzer import ResearchPaperAnalyzer
import os

st.set_page_config(page_title="Research Paper Analyzer", layout="wide")

st.title("🔬 AI-Powered Research Paper Analyzer")

# Initialize
if 'analyzer' not in st.session_state:
    api_key = os.getenv("OPENAI_API_KEY")
    st.session_state.analyzer = ResearchPaperAnalyzer(api_key)

# File upload
uploaded_files = st.file_uploader(
    "Upload Research Papers (PDF)", 
    type=['pdf'],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"Analyzing {uploaded_file.name}..."):
            # Save temp file
            with open(f"temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract and analyze
            text = st.session_state.analyzer.extract_text_from_pdf(
                f"temp_{uploaded_file.name}"
            )
            summary = st.session_state.analyzer.generate_summary(text)
            statistics = st.session_state.analyzer.extract_statistics(text)
            
            # Display results
            st.subheader(f"📄 {summary.get('title', 'Unknown Title')}")
            st.write(f"**Authors:** {summary.get('authors', 'Unknown')}")
            
            with st.expander("Abstract"):
                st.write(summary.get('abstract', 'N/A'))
            
            with st.expander("Key Findings"):
                for finding in summary.get('key_findings', []):
                    st.write(f"• {finding}")
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sample Size", 
                         statistics.get('sample_sizes', ['N/A'])[0])
            with col2:
                st.metric("P-Value", 
                         f"{min(statistics.get('p_values', [1])):.4f}")
            with col3:
                significance = st.session_state.analyzer.analyze_statistical_significance(statistics)
                st.metric("Significance", 
                         "✓ Yes" if significance['is_significant'] else "✗ No")
            
            # Visualizations
            figures = st.session_state.analyzer.create_visualizations(
                statistics, summary
            )
            for fig in figures:
                st.plotly_chart(fig, use_container_width=True)

# Run with: streamlit run app.py