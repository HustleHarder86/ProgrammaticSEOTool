"""Improved Streamlit wizard interface for Programmatic SEO Tool."""
import streamlit as st
import asyncio
import pandas as pd
import requests
import json
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Programmatic SEO Wizard",
    page_icon="🚀",
    layout="wide"
)

# API URL (adjust for deployment)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state
if 'wizard_step' not in st.session_state:
    st.session_state.wizard_step = 1
if 'business_info' not in st.session_state:
    st.session_state.business_info = None
if 'strategies' not in st.session_state:
    st.session_state.strategies = []
if 'selected_strategies' not in st.session_state:
    st.session_state.selected_strategies = []
if 'generated_keywords' not in st.session_state:
    st.session_state.generated_keywords = {}
if 'selected_keywords' not in st.session_state:
    st.session_state.selected_keywords = []
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []

# Title and description
st.title("🚀 Programmatic SEO Wizard")
st.markdown("Create thousands of SEO-optimized pages in 4 simple steps")

# Progress bar
progress = st.session_state.wizard_step / 4
st.progress(progress)

# Step indicators
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.session_state.wizard_step == 1:
        st.markdown("**Step 1: Analyze Business** 🔍")
    else:
        st.markdown("Step 1: Analyze Business ✅")
with col2:
    if st.session_state.wizard_step == 2:
        st.markdown("**Step 2: Choose Strategies** 📊")
    elif st.session_state.wizard_step > 2:
        st.markdown("Step 2: Choose Strategies ✅")
    else:
        st.markdown("Step 2: Choose Strategies")
with col3:
    if st.session_state.wizard_step == 3:
        st.markdown("**Step 3: Generate Content** ✍️")
    elif st.session_state.wizard_step > 3:
        st.markdown("Step 3: Generate Content ✅")
    else:
        st.markdown("Step 3: Generate Content")
with col4:
    if st.session_state.wizard_step == 4:
        st.markdown("**Step 4: Export & Publish** 📤")
    else:
        st.markdown("Step 4: Export & Publish")

st.markdown("---")

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

# Step 1: Business Analysis
if st.session_state.wizard_step == 1:
    st.header("Step 1: Tell Us About Your Business")
    st.markdown("We'll analyze your business to create the perfect SEO strategy")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_type = st.radio("How would you like to provide information?", 
                             ["Describe Your Business", "Enter Website URL"],
                             horizontal=True)
        
        if input_type == "Describe Your Business":
            business_description = st.text_area(
                "Business Description",
                placeholder="Example: We are a real estate investment SaaS platform that helps investors analyze properties, calculate ROI, and manage their portfolios. We serve real estate investors, property managers, and REITs across the United States...",
                height=200,
                help="Be specific about your services, products, target audience, and locations"
            )
            
            if st.button("Analyze Business", type="primary", disabled=not business_description):
                with st.spinner("🤖 Analyzing your business..."):
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
                            st.success("✅ Business analysis complete!")
                            st.session_state.wizard_step = 2
                            st.rerun()
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        else:  # Website URL
            website_url = st.text_input(
                "Website URL",
                placeholder="https://example.com",
                help="We'll scan your website to understand your business"
            )
            
            if st.button("Scan Website", type="primary", disabled=not website_url):
                with st.spinner("🔍 Scanning your website..."):
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
                            st.success("✅ Website analysis complete!")
                            st.session_state.wizard_step = 2
                            st.rerun()
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.info("""
        **Tips for better results:**
        - Include your main services/products
        - Mention your target audience
        - Specify locations you serve
        - Describe what makes you unique
        """)

# Step 2: Keyword Strategy Selection
elif st.session_state.wizard_step == 2:
    st.header("Step 2: Choose Your SEO Strategies")
    st.markdown("Based on your business, we've identified these programmatic SEO opportunities:")
    
    # Generate strategies if not already done
    if not st.session_state.strategies:
        with st.spinner("🧠 Generating intelligent SEO strategies..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/generate-strategies",
                    json=st.session_state.business_info
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.strategies = data["strategies"]
                else:
                    st.error(f"Error generating strategies: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display strategies as cards
    if st.session_state.strategies:
        # Add select all/none buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("Select All"):
                st.session_state.selected_strategies = [s['name'] for s in st.session_state.strategies]
                st.rerun()
        with col2:
            if st.button("Select None"):
                st.session_state.selected_strategies = []
                st.rerun()
        
        st.markdown("---")
        
        # Display strategy cards in a grid
        for i in range(0, len(st.session_state.strategies), 2):
            cols = st.columns(2)
            
            for j, col in enumerate(cols):
                if i + j < len(st.session_state.strategies):
                    strategy = st.session_state.strategies[i + j]
                    
                    with col:
                        # Create a card-like container
                        with st.container():
                            # Card header with checkbox
                            is_selected = strategy['name'] in st.session_state.selected_strategies
                            
                            col_check, col_icon, col_title = st.columns([1, 1, 8])
                            with col_check:
                                if st.checkbox("", key=f"strategy_{i+j}", value=is_selected):
                                    if strategy['name'] not in st.session_state.selected_strategies:
                                        st.session_state.selected_strategies.append(strategy['name'])
                                else:
                                    if strategy['name'] in st.session_state.selected_strategies:
                                        st.session_state.selected_strategies.remove(strategy['name'])
                            
                            with col_icon:
                                st.markdown(f"<h1>{strategy['icon']}</h1>", unsafe_allow_html=True)
                            
                            with col_title:
                                st.subheader(strategy['name'])
                            
                            # Card body
                            st.markdown(f"**{strategy['description']}**")
                            
                            # Estimated pages
                            st.metric("Estimated Pages", f"{strategy['estimated_pages']:,}")
                            
                            # Example URLs
                            with st.expander("Example URLs"):
                                for example in strategy['examples'][:3]:
                                    st.code(f"/{example}", language="text")
                            
                            st.markdown("---")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Back", type="secondary"):
                st.session_state.wizard_step = 1
                st.rerun()
        
        with col3:
            if st.button("Generate Keywords →", type="primary", 
                        disabled=len(st.session_state.selected_strategies) == 0):
                with st.spinner("🔍 Generating keywords for selected strategies..."):
                    # Generate keywords for each selected strategy
                    for strategy in st.session_state.strategies:
                        if strategy['name'] in st.session_state.selected_strategies:
                            try:
                                response = requests.post(
                                    f"{API_URL}/api/generate-keywords-for-strategy",
                                    json={
                                        "strategy": strategy,
                                        "business_info": st.session_state.business_info,
                                        "limit": 20  # Generate 20 keywords per strategy
                                    }
                                )
                                if response.status_code == 200:
                                    data = response.json()
                                    st.session_state.generated_keywords[strategy['name']] = data['keywords']
                            except Exception as e:
                                st.error(f"Error generating keywords for {strategy['name']}: {str(e)}")
                    
                    st.session_state.wizard_step = 3
                    st.rerun()
        
        # Show selected count
        if st.session_state.selected_strategies:
            st.info(f"✅ {len(st.session_state.selected_strategies)} strategies selected")

# Step 3: Content Generation
elif st.session_state.wizard_step == 3:
    st.header("Step 3: Review Keywords & Generate Content")
    
    # Display keywords grouped by strategy
    total_keywords = sum(len(kws) for kws in st.session_state.generated_keywords.values())
    st.markdown(f"Generated **{total_keywords}** keywords across **{len(st.session_state.generated_keywords)}** strategies")
    
    # Add select all/none for keywords
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("Select All Keywords"):
            st.session_state.selected_keywords = []
            for strategy_name, keywords in st.session_state.generated_keywords.items():
                for kw in keywords:
                    st.session_state.selected_keywords.append({
                        'strategy': strategy_name,
                        'keyword': kw['keyword'],
                        'data': kw
                    })
            st.rerun()
    with col2:
        if st.button("Clear Selection"):
            st.session_state.selected_keywords = []
            st.rerun()
    
    st.markdown("---")
    
    # Display keywords by strategy
    for strategy_name, keywords in st.session_state.generated_keywords.items():
        with st.expander(f"{strategy_name} ({len(keywords)} keywords)", expanded=True):
            # Select all for this strategy
            if st.checkbox(f"Select all in {strategy_name}", key=f"all_{strategy_name}"):
                for kw in keywords:
                    kw_entry = {
                        'strategy': strategy_name,
                        'keyword': kw['keyword'],
                        'data': kw
                    }
                    if kw_entry not in st.session_state.selected_keywords:
                        st.session_state.selected_keywords.append(kw_entry)
            
            # Display keywords in a table-like format
            for idx, kw in enumerate(keywords):
                col1, col2, col3, col4 = st.columns([1, 4, 2, 2])
                
                kw_entry = {
                    'strategy': strategy_name,
                    'keyword': kw['keyword'],
                    'data': kw
                }
                
                with col1:
                    is_selected = any(k['keyword'] == kw['keyword'] for k in st.session_state.selected_keywords)
                    if st.checkbox("", key=f"kw_{strategy_name}_{idx}", value=is_selected):
                        if not any(k['keyword'] == kw['keyword'] for k in st.session_state.selected_keywords):
                            st.session_state.selected_keywords.append(kw_entry)
                    else:
                        st.session_state.selected_keywords = [
                            k for k in st.session_state.selected_keywords 
                            if k['keyword'] != kw['keyword']
                        ]
                
                with col2:
                    st.write(kw['keyword'])
                
                with col3:
                    if 'search_volume_estimate' in kw:
                        volume_color = {
                            'high': '🟢',
                            'medium': '🟡', 
                            'low': '🔴'
                        }.get(kw['search_volume_estimate'], '⚪')
                        st.write(f"{volume_color} Volume: {kw['search_volume_estimate']}")
                
                with col4:
                    if 'competition' in kw:
                        comp_color = {
                            'low': '🟢',
                            'medium': '🟡',
                            'high': '🔴'
                        }.get(kw['competition'], '⚪')
                        st.write(f"{comp_color} Competition: {kw['competition']}")
    
    st.markdown("---")
    
    # Content generation options
    if st.session_state.selected_keywords:
        st.subheader("Content Generation Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            content_length = st.select_slider(
                "Content Length",
                options=["Short (500-1000 words)", "Medium (1000-2000 words)", "Long (2000+ words)"],
                value="Medium (1000-2000 words)"
            )
        
        with col2:
            include_schema = st.checkbox("Include Schema Markup", value=True)
            include_images = st.checkbox("Generate Image Suggestions", value=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back", type="secondary"):
            st.session_state.wizard_step = 2
            st.rerun()
    
    with col3:
        selected_count = len(st.session_state.selected_keywords)
        if st.button(f"Generate {selected_count} Pages →", type="primary", 
                    disabled=selected_count == 0):
            st.session_state.wizard_step = 4
            st.rerun()
    
    # Show selection summary
    if st.session_state.selected_keywords:
        st.success(f"✅ {len(st.session_state.selected_keywords)} keywords selected for content generation")

# Step 4: Export and Publish
elif st.session_state.wizard_step == 4:
    st.header("Step 4: Export Your Content")
    
    # Generate content if not already done
    if not st.session_state.generated_content:
        with st.spinner(f"🚀 Generating content for {len(st.session_state.selected_keywords)} keywords..."):
            # Simulate content generation (in production, this would call the API)
            st.session_state.generated_content = []
            for kw_data in st.session_state.selected_keywords[:10]:  # Limit for demo
                content = {
                    "keyword": kw_data['keyword'],
                    "strategy": kw_data['strategy'],
                    "title": kw_data['data'].get('title', f"{kw_data['keyword']} - Complete Guide"),
                    "url_slug": kw_data['data'].get('url_slug', kw_data['keyword'].lower().replace(' ', '-')),
                    "meta_description": f"Everything you need to know about {kw_data['keyword']}",
                    "content_preview": f"This comprehensive guide covers {kw_data['keyword']}...",
                    "word_count": 1500,
                    "status": "ready"
                }
                st.session_state.generated_content.append(content)
    
    # Display summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pages", len(st.session_state.generated_content))
    with col2:
        total_words = sum(c.get('word_count', 0) for c in st.session_state.generated_content)
        st.metric("Total Words", f"{total_words:,}")
    with col3:
        strategies_used = len(set(c['strategy'] for c in st.session_state.generated_content))
        st.metric("Strategies Used", strategies_used)
    
    st.markdown("---")
    
    # Export options
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox(
            "Export Format",
            ["CSV (Spreadsheet)", "WordPress XML", "JSON", "HTML Files", "Markdown Files"]
        )
        
        project_name = st.text_input("Project Name", value="programmatic_seo_content")
    
    with col2:
        if export_format == "WordPress XML":
            st.text_input("WordPress Author", value="admin")
            st.selectbox("Post Status", ["draft", "publish"])
        elif export_format == "HTML Files":
            st.checkbox("Include CSS Styling", value=True)
            st.checkbox("Create Index Page", value=True)
    
    # Preview content
    st.subheader("Content Preview")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["List View", "Preview", "Statistics"])
    
    with tab1:
        # Display content list
        df = pd.DataFrame(st.session_state.generated_content)
        st.dataframe(
            df[['title', 'strategy', 'word_count', 'status']],
            use_container_width=True
        )
    
    with tab2:
        # Show content preview
        if st.session_state.generated_content:
            selected_preview = st.selectbox(
                "Select content to preview",
                [c['title'] for c in st.session_state.generated_content]
            )
            
            for content in st.session_state.generated_content:
                if content['title'] == selected_preview:
                    st.markdown(f"### {content['title']}")
                    st.markdown(f"**URL:** /{content['url_slug']}")
                    st.markdown(f"**Meta Description:** {content['meta_description']}")
                    st.markdown("---")
                    st.markdown(content['content_preview'])
    
    with tab3:
        # Show statistics by strategy
        strategy_stats = {}
        for content in st.session_state.generated_content:
            strategy = content['strategy']
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {'count': 0, 'words': 0}
            strategy_stats[strategy]['count'] += 1
            strategy_stats[strategy]['words'] += content.get('word_count', 0)
        
        for strategy, stats in strategy_stats.items():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**{strategy}**")
            with col2:
                st.metric("Pages", stats['count'])
            with col3:
                st.metric("Words", f"{stats['words']:,}")
    
    st.markdown("---")
    
    # Export button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back", type="secondary"):
            st.session_state.wizard_step = 3
            st.rerun()
    
    with col3:
        if st.button(f"Export as {export_format}", type="primary"):
            # Handle export based on format
            if export_format == "CSV (Spreadsheet)":
                df = pd.DataFrame(st.session_state.generated_content)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            elif export_format == "JSON":
                json_data = json.dumps(st.session_state.generated_content, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            st.success("✅ Export complete! Your content is ready for publishing.")
    
    # Success message
    with st.container():
        st.success(f"""
        🎉 **Congratulations!** You've successfully generated {len(st.session_state.generated_content)} SEO-optimized pages.
        
        **Next Steps:**
        1. Download your content using the export button above
        2. Review and customize the content as needed
        3. Publish to your website
        4. Monitor rankings and traffic
        """)
        
        if st.button("Start New Campaign", type="secondary"):
            # Reset session state
            st.session_state.wizard_step = 1
            st.session_state.business_info = None
            st.session_state.strategies = []
            st.session_state.selected_strategies = []
            st.session_state.generated_keywords = {}
            st.session_state.selected_keywords = []
            st.session_state.generated_content = []
            st.rerun()

# Sidebar with tips
st.sidebar.title("💡 Pro Tips")

if st.session_state.wizard_step == 1:
    st.sidebar.info("""
    **Step 1 Tips:**
    - Be specific about your services
    - Include your location if relevant
    - Mention your target audience
    - List your main competitors
    """)
elif st.session_state.wizard_step == 2:
    st.sidebar.info("""
    **Step 2 Tips:**
    - Choose strategies that match your expertise
    - Consider search volume potential
    - Mix informational and commercial intent
    - Start with 2-3 strategies to test
    """)
elif st.session_state.wizard_step == 3:
    st.sidebar.info("""
    **Step 3 Tips:**
    - Focus on keywords with low competition
    - Consider user search intent
    - Group related keywords together
    - Quality over quantity
    """)
elif st.session_state.wizard_step == 4:
    st.sidebar.info("""
    **Step 4 Tips:**
    - Review content before publishing
    - Set up analytics tracking
    - Create an XML sitemap
    - Monitor initial rankings
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ for SEO automation")