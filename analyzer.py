"""
Mock Research Paper Analyzer - Works WITHOUT OpenAI API
Use this version to test the interface without API credits
"""

import os
import PyPDF2
import json
import re
from typing import Dict, List, Any
import time

class ResearchPaperAnalyzer:
    """Analyzes research papers - MOCK VERSION"""
    
    def __init__(self, api_key: str):
        """Initialize - doesn't actually need API key for mock"""
        self.api_key = api_key
        print("🧪 Running in MOCK MODE - Using sample data instead of real AI")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
        
        return text
    
    def generate_summary(self, text: str) -> Dict[str, Any]:
        """Generate MOCK summary of the paper"""
        
        # Simulate processing time
        time.sleep(2)
        
        # Try to extract title from first few lines
        lines = text.split('\n')
        potential_title = lines[0][:100] if lines else "Research Paper Analysis"
        
        # Create mock summary based on actual text
        return {
            "title": potential_title,
            "authors": "Authors extracted from PDF",
            "abstract": "This paper presents novel findings in the field. The study demonstrates significant improvements over baseline methods. Key contributions include theoretical framework and empirical validation across multiple datasets.",
            "methodology": "The research employs a mixed-methods approach combining quantitative analysis with qualitative insights. Data was collected from multiple sources and analyzed using statistical techniques.",
            "key_findings": [
                "Significant improvement in primary metrics compared to baseline",
                "Novel approach demonstrates scalability across different contexts",
                "Results validated through rigorous statistical testing",
                "Findings have practical implications for real-world applications",
                "Strong correlation found between key variables"
            ],
            "conclusions": "The study successfully demonstrates the effectiveness of the proposed approach. Results suggest promising directions for future research and practical applications in the field."
        }
    
    def extract_statistics(self, text: str) -> Dict[str, Any]:
        """Extract statistical information from paper using REGEX"""
        
        # Simulate processing time
        time.sleep(1)
        
        # Use regex to find actual statistics in the text
        stats = self._regex_extract_stats(text)
        
        # If no stats found, add some mock data
        if not stats['sample_sizes']:
            stats['sample_sizes'] = [500, 250]
        if not stats['p_values']:
            stats['p_values'] = [0.003, 0.012, 0.041]
        if not stats['percentages']:
            stats['percentages'] = [85.5, 72.3, 91.2, 67.8]
        
        return stats
    
    def _regex_extract_stats(self, text: str) -> Dict[str, Any]:
        """Extract statistics using regex"""
        
        # Extract p-values
        p_values = []
        p_patterns = [
            r'p\s*[=<>]\s*([0-9.]+)',
            r'P\s*[=<>]\s*([0-9.]+)',
            r'p-value\s*[=:]\s*([0-9.]+)'
        ]
        for pattern in p_patterns:
            matches = re.findall(pattern, text[:5000])  # Only first 5000 chars
            for p in matches:
                try:
                    p_val = float(p)
                    if 0 <= p_val <= 1.0:
                        p_values.append(p_val)
                except:
                    pass
        
        # Extract sample sizes
        sample_sizes = []
        n_patterns = [
            r'[Nn]\s*=\s*(\d+)',
            r'sample size\s*[=:]\s*(\d+)',
            r'participants\s*[=:]\s*(\d+)',
            r'subjects\s*[=:]\s*(\d+)'
        ]
        for pattern in n_patterns:
            matches = re.findall(pattern, text[:5000])
            for n in matches:
                try:
                    n_val = int(n)
                    if n_val > 0 and n_val < 1000000:  # Reasonable range
                        sample_sizes.append(n_val)
                except:
                    pass
        
        # Extract percentages
        percentages = []
        perc_matches = re.findall(r'(\d+\.?\d*)\s*%', text[:5000])
        for p in perc_matches:
            try:
                p_val = float(p)
                if 0 <= p_val <= 100:
                    percentages.append(p_val)
            except:
                pass
        
        return {
            "sample_sizes": list(set(sample_sizes))[:10] if sample_sizes else [],
            "p_values": list(set(p_values))[:10] if p_values else [],
            "percentages": list(set(percentages))[:20] if percentages else [],
            "confidence_intervals": []
        }
    
    def analyze_statistical_significance(self, stats: Dict) -> Dict[str, Any]:
        """Analyze if results are statistically significant"""
        
        analysis = {
            "is_significant": False,
            "significance_level": 0.05,
            "interpretation": "No statistical data found",
            "min_p_value": None
        }
        
        p_values = stats.get("p_values", [])
        
        if p_values:
            min_p = min(p_values)
            analysis["min_p_value"] = min_p
            analysis["is_significant"] = min_p < 0.05
            
            if min_p < 0.001:
                analysis["interpretation"] = "Highly significant results (p < 0.001) - Very strong evidence"
            elif min_p < 0.01:
                analysis["interpretation"] = "Very significant results (p < 0.01) - Strong evidence"
            elif min_p < 0.05:
                analysis["interpretation"] = "Significant results (p < 0.05) - Moderate evidence"
            else:
                analysis["interpretation"] = "Not statistically significant (p ≥ 0.05) - Weak evidence"
        else:
            # Check sample sizes
            sample_sizes = stats.get("sample_sizes", [])
            if sample_sizes and max(sample_sizes) > 0:
                avg_sample = sum(sample_sizes) / len(sample_sizes)
                if avg_sample > 1000:
                    analysis["interpretation"] = f"Large sample size (avg: {int(avg_sample)}) - Good statistical power"
                elif avg_sample > 100:
                    analysis["interpretation"] = f"Moderate sample size (avg: {int(avg_sample)}) - Adequate for most analyses"
                else:
                    analysis["interpretation"] = f"Small sample size (avg: {int(avg_sample)}) - Limited statistical power"
            else:
                analysis["interpretation"] = "Using mock statistical data for demonstration"
        
        return analysis
    
    def create_comparison(self, papers_data: List[Dict]) -> Dict[str, Any]:
        """Compare multiple papers"""
        
        comparison = {
            "total_papers": len(papers_data),
            "papers": []
        }
        
        for paper in papers_data:
            paper_summary = {
                "title": paper.get("summary", {}).get("title", "Unknown"),
                "sample_size": 0,
                "min_p_value": 1.0,
                "is_significant": False
            }
            
            # Get statistics
            stats = paper.get("statistics", {})
            sample_sizes = stats.get("sample_sizes", [])
            if sample_sizes:
                paper_summary["sample_size"] = max(sample_sizes)
            
            p_values = stats.get("p_values", [])
            if p_values:
                paper_summary["min_p_value"] = min(p_values)
                paper_summary["is_significant"] = min(p_values) < 0.05
            
            comparison["papers"].append(paper_summary)
        
        # Calculate summary statistics
        if comparison["papers"]:
            comparison["avg_sample_size"] = sum(p["sample_size"] for p in comparison["papers"]) / len(comparison["papers"])
            comparison["significant_count"] = sum(1 for p in comparison["papers"] if p["is_significant"])
        
        return comparison


# Simple test function
def test_analyzer():
    """Test the analyzer with a sample"""
    print("🧪 Testing Mock Analyzer...")
    
    analyzer = ResearchPaperAnalyzer("mock_key")
    
    # Test with sample text
    sample_text = """
    Abstract: This study examines the effectiveness of a new teaching method.
    Method: We conducted a randomized controlled trial with n=500 students.
    Results: The treatment group showed significant improvement (p=0.003).
    The average test score increased by 15.5%.
    Conclusion: The new method is highly effective.
    """
    
    print("Testing analyzer...")
    summary = analyzer.generate_summary(sample_text)
    print(f"✓ Summary generated: {summary.get('title')[:50]}...")
    
    stats = analyzer.extract_statistics(sample_text)
    print(f"✓ Statistics extracted: {len(stats.get('p_values', []))} p-values found")
    
    significance = analyzer.analyze_statistical_significance(stats)
    print(f"✓ Significance analyzed: {significance.get('interpretation')}")
    
    print("\n✅ Mock Analyzer is working correctly!")
    print("📝 Note: This uses sample data. Add OpenAI credits for real AI analysis.")


if __name__ == "__main__":
    test_analyzer()