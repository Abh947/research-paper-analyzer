"""
Complete Streamlit App for Research Paper Analyzer
Copy this ENTIRE file into app.py
"""

import streamlit as st
from analyzer import ResearchPaperAnalyzer
from dotenv import load_dotenv
import os
import tempfile
import pandas as pd

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Research Paper Analyzer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'analyzed_papers' not in st.session_state:
    st.session_state.analyzed_papers = {}

# Title
st.title("🔬 AI-Powered Research Paper Analyzer")
st.markdown("**Upload academic papers for instant AI-powered summaries and statistical analysis**")
st.markdown("---")

# Check API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "paste_your_key_here":
    st.error("⚠️ **OpenAI API Key Not Found!**")
    st.info("""
    **To fix this:**
    1. Open the `.env` file in VS Code
    2. Add your OpenAI API key: `OPENAI_API_KEY=sk-proj-your-key-here`
    3. Get a key from: https://platform.openai.com/api-keys
    4. Save the file and restart this app
    """)
    st.stop()

# Initialize analyzer
@st.cache_resource
def get_analyzer():
    return ResearchPaperAnalyzer(api_key)

try:
    analyzer = get_analyzer()
    st.sidebar.success("✅ API Connected")
except Exception as e:
    st.error(f"Error initializing analyzer: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("📁 Upload Papers")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more research papers in PDF format"
    )
    
    st.markdown("---")
    
    # Statistics
    st.subheader("📊 Dashboard")
    total_papers = len(st.session_state.analyzed_papers)
    st.metric("Papers Analyzed", total_papers)
    
    if uploaded_files:
        st.metric("Papers Uploaded", len(uploaded_files))
    
    st.markdown("---")
    
    # Clear button
    if st.button("🗑️ Clear All Data"):
        st.session_state.analyzed_papers = {}
        st.rerun()
    
    st.markdown("---")
    st.caption("Powered by OpenAI GPT-3.5")

# Main content area
if not uploaded_files:
    # Welcome screen
    st.info("👆 **Upload PDF files using the sidebar to get started**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📄 Step 1")
        st.write("Upload research papers in PDF format")
        st.write("✓ Multiple files supported")
        st.write("✓ Automatic text extraction")
    
    with col2:
        st.markdown("### 🤖 Step 2")
        st.write("AI analyzes your papers")
        st.write("✓ Generate summaries")
        st.write("✓ Extract statistics")
    
    with col3:
        st.markdown("### 📊 Step 3")
        st.write("View comprehensive analysis")
        st.write("✓ Key findings")
        st.write("✓ Statistical significance")
    
    # Example section
    with st.expander("📖 What can this tool do?", expanded=False):
        st.markdown("""
        **This tool helps researchers by:**
        - 📝 Generating concise summaries of academic papers
        - 📊 Extracting statistical information (p-values, sample sizes, etc.)
        - 🔍 Identifying key findings and methodology
        - 📈 Analyzing statistical significance
        - 🔄 Comparing multiple papers side-by-side
        
        **Perfect for:**
        - Literature reviews
        - Research synthesis
        - Quick paper screening
        - Statistical analysis verification
        """)

else:
    # Process uploaded files
    for uploaded_file in uploaded_files:
        file_key = uploaded_file.name
        
        # Check if already analyzed
        if file_key not in st.session_state.analyzed_papers:
            with st.spinner(f"🔍 Analyzing **{uploaded_file.name}**... This may take 30-60 seconds..."):
                try:
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Extract text
                    with st.status("Extracting text from PDF..."):
                        text = analyzer.extract_text_from_pdf(tmp_path)
                    
                    if not text or len(text) < 100:
                        st.error(f"⚠️ Could not extract enough text from {uploaded_file.name}")
                        st.info("The PDF might be scanned images or protected. Try a different file.")
                        continue
                    
                    # Generate summary
                    with st.status("Generating AI summary..."):
                        summary = analyzer.generate_summary(text)
                    
                    # Extract statistics
                    with st.status("Extracting statistics..."):
                        statistics = analyzer.extract_statistics(text)
                    
                    # Analyze significance
                    with st.status("Analyzing statistical significance..."):
                        significance = analyzer.analyze_statistical_significance(statistics)
                    
                    # Store results
                    st.session_state.analyzed_papers[file_key] = {
                        'summary': summary,
                        'statistics': statistics,
                        'significance': significance,
                        'file_name': uploaded_file.name
                    }
                    
                    # Clean up
                    os.unlink(tmp_path)
                    
                    st.success(f"✅ Successfully analyzed: {uploaded_file.name}")
                    
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}")
                    st.error(f"Error details: {str(e)}")
                    continue
    
    # Display results in tabs
    tab1, tab2, tab3 = st.tabs(["📝 Summaries", "📊 Statistical Analysis", "🔄 Compare Papers"])
    
    with tab1:
        st.header("📝 Paper Summaries")
        
        if not st.session_state.analyzed_papers:
            st.info("No papers analyzed yet. Upload PDFs to begin.")
        else:
            for file_name, data in st.session_state.analyzed_papers.items():
                with st.expander(f"📄 **{file_name}**", expanded=True):
                    summary = data['summary']
                    
                    # Title and authors
                    st.markdown(f"## {summary.get('title', 'Untitled Paper')}")
                    st.markdown(f"**Authors:** {summary.get('authors', 'Unknown')}")
                    st.markdown("---")
                    
                    # Abstract
                    st.markdown("### 📋 Abstract")
                    st.write(summary.get('abstract', 'N/A'))
                    
                    # Methodology
                    st.markdown("### 🔬 Methodology")
                    st.write(summary.get('methodology', 'N/A'))
                    
                    # Key findings
                    st.markdown("### 🎯 Key Findings")
                    findings = summary.get('key_findings', [])
                    if isinstance(findings, list):
                        for i, finding in enumerate(findings, 1):
                            st.markdown(f"{i}. {finding}")
                    else:
                        st.write(findings)
                    
                    # Conclusions
                    st.markdown("### 💡 Conclusions")
                    st.write(summary.get('conclusions', 'N/A'))
    
    with tab2:
        st.header("📊 Statistical Analysis")
        
        if not st.session_state.analyzed_papers:
            st.info("No papers analyzed yet. Upload PDFs to begin.")
        else:
            for file_name, data in st.session_state.analyzed_papers.items():
                with st.expander(f"📊 **{file_name}**", expanded=True):
                    stats = data['statistics']
                    significance = data['significance']
                    
                    # Metrics in columns
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        sample_sizes = stats.get('sample_sizes', [])
                        if sample_sizes and max(sample_sizes) > 0:
                            st.metric("📊 Sample Size", f"{max(sample_sizes):,}")
                        else:
                            st.metric("📊 Sample Size", "Not found")
                    
                    with col2:
                        p_values = stats.get('p_values', [])
                        if p_values:
                            st.metric("🎯 Min P-Value", f"{min(p_values):.4f}")
                        else:
                            st.metric("🎯 P-Value", "Not found")
                    
                    with col3:
                        is_sig = significance.get('is_significant', False)
                        st.metric(
                            "✓ Significant?",
                            "Yes ✅" if is_sig else "No ❌"
                        )
                    
                    with col4:
                        percentages = stats.get('percentages', [])
                        if percentages:
                            st.metric("📈 Max Value", f"{max(percentages):.1f}%")
                        else:
                            st.metric("📈 Values", "Not found")
                    
                    st.markdown("---")
                    
                    # Interpretation
                    st.markdown("### 💬 Interpretation")
                    interpretation = significance.get('interpretation', 'No interpretation available')
                    
                    if 'significant' in interpretation.lower() and 'not' not in interpretation.lower():
                        st.success(f"✅ {interpretation}")
                    elif 'not significant' in interpretation.lower():
                        st.warning(f"⚠️ {interpretation}")
                    else:
                        st.info(f"ℹ️ {interpretation}")
                    
                    # Detailed statistics (moved outside the expander)
                    st.markdown("---")
                    st.markdown("### 📋 Detailed Statistics")
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.markdown("**Sample Sizes Found:**")
                        if sample_sizes:
                            for size in sample_sizes[:5]:
                                st.write(f"• n = {size:,}")
                        else:
                            st.write("None found")
                    
                    with col_b:
                        st.markdown("**P-Values Found:**")
                        if p_values:
                            for pval in p_values[:5]:
                                st.write(f"• p = {pval:.4f}")
                        else:
                            st.write("None found")
                    
                    st.markdown("**Percentages Mentioned:**")
                    if percentages:
                        st.write(", ".join([f"{p:.1f}%" for p in percentages[:10]]))
                    else:
                        st.write("None found")
    
    with tab3:
        st.header("🔄 Compare Papers")
        
        num_papers = len(st.session_state.analyzed_papers)
        
        if num_papers == 0:
            st.info("No papers analyzed yet. Upload PDFs to begin.")
        elif num_papers == 1:
            st.info("Upload at least 2 papers to compare them side-by-side.")
        else:
            st.success(f"Comparing {num_papers} papers")
            
            # Create comparison table
            comparison_data = []
            
            for file_name, data in st.session_state.analyzed_papers.items():
                stats = data['statistics']
                summary = data['summary']
                significance = data['significance']
                
                sample_sizes = stats.get('sample_sizes', [0])
                p_values = stats.get('p_values', [1.0])
                
                comparison_data.append({
                    'Paper': file_name[:40] + "..." if len(file_name) > 40 else file_name,
                    'Sample Size': max(sample_sizes) if sample_sizes else 0,
                    'Min P-Value': min(p_values) if p_values else 1.0,
                    'Significant': '✅' if significance.get('is_significant') else '❌',
                    'Title': summary.get('title', 'Unknown')[:50]
                })
            
            # Display comparison table
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Comparison insights
            st.markdown("### 📈 Comparison Insights")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_significant = sum([1 for d in comparison_data if d['Significant'] == '✅'])
                st.metric(
                    "Papers with Significant Results",
                    f"{total_significant} / {num_papers}",
                    delta=f"{(total_significant/num_papers*100):.0f}%"
                )
            
            with col2:
                avg_sample = sum([d['Sample Size'] for d in comparison_data]) / len(comparison_data)
                st.metric("Average Sample Size", f"{avg_sample:,.0f}")
            
            with col3:
                avg_p = sum([d['Min P-Value'] for d in comparison_data if d['Min P-Value'] < 1.0])
                count_p = sum([1 for d in comparison_data if d['Min P-Value'] < 1.0])
                if count_p > 0:
                    st.metric("Average P-Value", f"{(avg_p/count_p):.4f}")
                else:
                    st.metric("Average P-Value", "N/A")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>Built with ❤️ using Streamlit, OpenAI GPT-3.5, and Python</p>
        <p>For educational and research purposes</p>
    </div>
""", unsafe_allow_html=True)