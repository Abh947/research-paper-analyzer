# 🔬 AI-Powered Research Paper Analyzer

An intelligent web application that uses OpenAI's GPT-3.5 to automatically analyze academic research papers, extract key findings, and provide statistical insights.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 📄 **PDF Upload & Processing** - Automatic text extraction from research papers
- 🤖 **AI-Powered Summaries** - GPT-3.5 generates structured summaries with title, authors, abstract, and key findings
- 📊 **Statistical Analysis** - Extracts p-values, sample sizes, percentages, and significance levels
- 🔄 **Multi-Paper Comparison** - Compare multiple papers side-by-side with visual analytics
- 📈 **Interactive Dashboard** - Clean, intuitive web interface built with Streamlit
- ⚡ **Real-time Processing** - Analysis completed in 30-60 seconds per paper

## 🎥 Demo

[Add your demo video or screenshots here]

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** - Web framework
- **OpenAI GPT-3.5-turbo** - AI analysis
- **PyPDF2** - PDF text extraction
- **Pandas** - Data processing
- **Regular Expressions** - Statistical pattern matching

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/research-paper-analyzer.git
cd research-paper-analyzer
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_api_key_here
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Upload Papers** - Click "Browse files" in the sidebar and select PDF research papers
2. **Wait for Analysis** - The AI will process the paper (takes 30-60 seconds)
3. **View Results** - Explore three tabs:
   - **Summaries** - AI-generated paper summaries
   - **Statistical Analysis** - Extracted metrics and significance
   - **Compare Papers** - Side-by-side comparison of multiple papers

## 🏗️ Project Structure
```
research-paper-analyzer/
├── app.py                  # Main Streamlit application
├── analyzer.py             # Core analysis logic
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── data/                  # Uploaded PDFs (not in repo)
└── outputs/               # Analysis results (not in repo)
```

## 🔑 Key Features Explained

### AI Summarization
Uses GPT-3.5-turbo with engineered prompts to extract:
- Paper title and authors
- Concise abstract (2-3 sentences)
- Methodology description
- 3-5 key findings
- Conclusions

### Statistical Extraction
Dual approach for accuracy:
1. **AI extraction** - GPT-3.5 identifies statistics
2. **Regex validation** - Pattern matching confirms values

Extracts:
- P-values (various formats: p=0.05, P<0.001, etc.)
- Sample sizes (n=500, participants=1000, etc.)
- Percentages and confidence intervals

### Significance Analysis
Automatically determines if results are statistically significant:
- p < 0.001: Highly significant
- p < 0.01: Very significant
- p < 0.05: Significant
- p ≥ 0.05: Not significant

## 💡 How It Works
```
User Upload → PDF Extraction → AI Analysis → Results Display
     ↓              ↓               ↓              ↓
  Browser      PyPDF2 reads    GPT-3.5       Streamlit
              text content    summarizes      Dashboard
                                ↓
                          Regex extracts
                           statistics
```

## 📊 Use Cases

- 📚 **Literature Reviews** - Quickly screen and summarize papers
- 🎓 **Academic Research** - Extract key findings from studies
- 🔍 **Statistical Verification** - Check reported statistics
- 📝 **Meta-Analysis** - Compare methodologies across papers
- 👨‍🎓 **Student Projects** - Understand complex papers faster

## 🚀 Future Enhancements

- [ ] Citation network visualization
- [ ] Support for Word/HTML documents
- [ ] Batch processing for 50+ papers
- [ ] Export results to PDF/Excel
- [ ] Topic modeling across papers
- [ ] Multi-language support
- [ ] Fine-tuned model for academic papers

## ⚠️ Limitations

- Requires OpenAI API credits (~$0.05 per paper)
- Works best with text-based PDFs (not scanned images)
- Limited to papers under ~20 pages for optimal performance
- May occasionally miss statistics in unusual formats

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- OpenAI for providing GPT-3.5 API
- Streamlit for the excellent web framework
- The open-source community for various Python libraries

## 📞 Support

If you encounter any issues or have questions:
1. Check existing [Issues](https://github.com/YOUR_USERNAME/research-paper-analyzer/issues)
2. Create a new issue with details
3. Contact me via email

---

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ and Python