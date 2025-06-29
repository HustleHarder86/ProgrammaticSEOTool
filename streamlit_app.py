"""Streamlit UI for Programmatic SEO Tool."""
import streamlit as st
import asyncio
import pandas as pd
import requests
import json
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Programmatic SEO Tool",
    page_icon="🚀",
    layout="wide"
)

# API URL (adjust for deployment)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state
if 'business_info' not in st.session_state:
    st.session_state.business_info = None
if 'opportunities' not in st.session_state:
    st.session_state.opportunities = []
if 'selected_keywords' not in st.session_state:
    st.session_state.selected_keywords = []
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []

# Title and description
st.title("🚀 Programmatic SEO Tool")
st.markdown("Generate thousands of SEO-optimized pages automatically")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Business Analysis", "Keyword Selection", "Content Generation", "Export"])

# Check API health
try:
    health_response = requests.get(f"{API_URL}/health")
    if health_response.status_code == 200:
        health_data = health_response.json()
        if not health_data.get("ai_provider"):
            st.error("⚠️ No AI provider configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file")
    else:
        st.error("⚠️ API is not responding. Make sure the FastAPI server is running.")
except:
    st.error("⚠️ Cannot connect to API. Make sure the FastAPI server is running on http://localhost:8000")

# Business Analysis Page
if page == "Business Analysis":
    st.header("📊 Business Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        input_type = st.radio("Input Method", ["Text Description", "Website URL"])
    
    if input_type == "Text Description":
        business_description = st.text_area(
            "Describe your business",
            placeholder="We are a digital marketing agency in Austin, Texas specializing in SEO, content marketing, and social media management...",
            height=200
        )
        analyze_button = st.button("Analyze Business", type="primary")
        
        if analyze_button and business_description:
            with st.spinner("Analyzing your business..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/analyze-business",
                        json={
                            "input_type": "text",
                            "content": business_description
                        }
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.business_info = data["business_info"]
                        st.session_state.opportunities = data["opportunities"]
                        st.success("✅ Business analysis complete!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    else:  # Website URL
        website_url = st.text_input(
            "Enter your website URL",
            placeholder="https://example.com"
        )
        analyze_button = st.button("Scan Website", type="primary")
        
        if analyze_button and website_url:
            with st.spinner("Scanning your website..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/analyze-business",
                        json={
                            "input_type": "url",
                            "content": website_url
                        }
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.business_info = data["business_info"]
                        st.session_state.opportunities = data["opportunities"]
                        st.success("✅ Website analysis complete!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Display results
    if st.session_state.business_info:
        with col2:
            st.subheader("Business Information")
            info = st.session_state.business_info
            
            if info.get("name"):
                st.write(f"**Name:** {info['name']}")
            if info.get("industry"):
                st.write(f"**Industry:** {info['industry']}")
            if info.get("location"):
                st.write(f"**Location:** {info['location']}")
            
            if info.get("services"):
                st.write("**Services:**")
                for service in info["services"][:5]:
                    st.write(f"- {service}")
            
            if info.get("keywords"):
                st.write("**Key Terms:**")
                st.write(", ".join(info["keywords"][:10]))
        
        st.subheader(f"📈 Content Opportunities ({len(st.session_state.opportunities)} found)")
        
        if st.session_state.opportunities:
            df = pd.DataFrame(st.session_state.opportunities)
            df = df[["keyword", "content_type", "priority", "description"]]
            st.dataframe(df, use_container_width=True)

# Keyword Selection Page
elif page == "Keyword Selection":
    st.header("🔍 Keyword Selection")
    
    if not st.session_state.opportunities:
        st.warning("Please complete business analysis first")
    else:
        st.subheader("Select Keywords to Target")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            content_types = ["All"] + list(set(opp["content_type"] for opp in st.session_state.opportunities))
            selected_type = st.selectbox("Content Type", content_types)
        
        with col2:
            min_priority = st.slider("Minimum Priority", 1, 10, 5)
        
        with col3:
            max_keywords = st.number_input("Max Keywords", min_value=1, max_value=100, value=20)
        
        # Filter opportunities
        filtered_opps = st.session_state.opportunities
        if selected_type != "All":
            filtered_opps = [opp for opp in filtered_opps if opp["content_type"] == selected_type]
        filtered_opps = [opp for opp in filtered_opps if opp["priority"] >= min_priority]
        filtered_opps = filtered_opps[:max_keywords]
        
        # Display selectable keywords
        st.write(f"Showing {len(filtered_opps)} keywords")
        
        selected = []
        for idx, opp in enumerate(filtered_opps):
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            with col1:
                if st.checkbox("", key=f"kw_{idx}"):
                    selected.append(opp)
            with col2:
                st.write(opp["keyword"])
            with col3:
                st.write(opp["content_type"])
            with col4:
                st.write(f"Priority: {opp['priority']}")
        
        if st.button("Save Selected Keywords", type="primary"):
            st.session_state.selected_keywords = selected
            st.success(f"✅ {len(selected)} keywords selected")

# Content Generation Page
elif page == "Content Generation":
    st.header("✍️ Content Generation")
    
    if not st.session_state.selected_keywords:
        st.warning("Please select keywords first")
    else:
        st.subheader(f"Generate Content for {len(st.session_state.selected_keywords)} Keywords")
        
        col1, col2 = st.columns(2)
        with col1:
            template_type = st.selectbox(
                "Content Template",
                ["comparison", "how-to", "best-x-for-y", "location-based", "ultimate-guide"]
            )
        
        with col2:
            variations = st.number_input("Variations per keyword", min_value=1, max_value=3, value=1)
        
        if st.button("Generate Content", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            generated_content = []
            total_keywords = len(st.session_state.selected_keywords)
            
            for idx, keyword_data in enumerate(st.session_state.selected_keywords):
                status_text.text(f"Generating content for: {keyword_data['keyword']}")
                
                try:
                    # This would call the actual API endpoint
                    # For now, we'll create placeholder content
                    content = {
                        "keyword": keyword_data["keyword"],
                        "title": f"{keyword_data['keyword']} - Complete Guide",
                        "meta_description": f"Learn everything about {keyword_data['keyword']}",
                        "slug": keyword_data["keyword"].lower().replace(" ", "-"),
                        "content_markdown": f"# {keyword_data['keyword']}\n\nContent would be generated here...",
                        "content_html": f"<h1>{keyword_data['keyword']}</h1><p>Content would be generated here...</p>",
                        "word_count": 2000,
                        "template_used": template_type,
                        "status": "ready"
                    }
                    generated_content.append(content)
                    
                except Exception as e:
                    st.error(f"Error generating content for {keyword_data['keyword']}: {str(e)}")
                
                progress_bar.progress((idx + 1) / total_keywords)
            
            st.session_state.generated_content = generated_content
            status_text.text(f"✅ Generated {len(generated_content)} content pieces!")
            
            # Display preview
            if generated_content:
                st.subheader("Content Preview")
                for content in generated_content[:3]:
                    with st.expander(content["title"]):
                        st.write(f"**Slug:** {content['slug']}")
                        st.write(f"**Meta Description:** {content['meta_description']}")
                        st.write(f"**Word Count:** {content['word_count']}")
                        st.markdown("---")
                        st.markdown(content["content_markdown"][:500] + "...")

# Export Page
elif page == "Export":
    st.header("📤 Export Content")
    
    if not st.session_state.generated_content:
        st.warning("Please generate content first")
    else:
        st.subheader(f"Export {len(st.session_state.generated_content)} Content Pieces")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_format = st.selectbox("Export Format", ["CSV", "WordPress XML", "JSON"])
            project_name = st.text_input("Project Name", value="SEO_Content")
        
        if st.button("Export Content", type="primary"):
            try:
                if export_format == "CSV":
                    # Create CSV content
                    df = pd.DataFrame(st.session_state.generated_content)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                elif export_format == "JSON":
                    # Create JSON content
                    json_data = json.dumps(st.session_state.generated_content, indent=2)
                    
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                st.success("✅ Export ready for download!")
                
            except Exception as e:
                st.error(f"Error exporting: {str(e)}")
        
        # Display export preview
        with col2:
            st.subheader("Export Preview")
            df = pd.DataFrame(st.session_state.generated_content)
            if not df.empty:
                st.write(f"**Total Pieces:** {len(df)}")
                st.write(f"**Total Words:** {df['word_count'].sum():,}")
                st.write(f"**Templates Used:** {', '.join(df['template_used'].unique())}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ for SEO automation")