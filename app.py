"""
Streamlit frontend for ShopAssist RAG
"""
import streamlit as st
import time
from src.rag_pipeline import RAGPipeline

# Page config
st.set_page_config(
    page_title="ShopAssist RAG",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .query-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .answer-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .source-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# Initialize pipeline
@st.cache_resource
def load_pipeline():
    """Load RAG pipeline (cached)"""
    return RAGPipeline()


def display_source(source, index):
    """Display a single source document"""
    with st.expander(f"📄 Source {index + 1}: {source['type'].upper()} (Relevance: {source['score']:.2%})"):
        st.markdown(f"**Preview:**")
        st.text(source['content_preview'])
        
        st.markdown("**Metadata:**")
        metadata = source['metadata']
        
        if source['type'] == 'product':
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Title:** {metadata.get('title', 'N/A')}")
                st.write(f"**Brand:** {metadata.get('brand', 'N/A')}")
            with col2:
                st.write(f"**Price:** {metadata.get('price', 'N/A')}")
                st.write(f"**Category:** {metadata.get('category', 'N/A')}")
        
        elif source['type'] == 'review':
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Rating:** {metadata.get('rating', 'N/A')}/5 ⭐")
            with col2:
                st.write(f"**Reviewer:** {metadata.get('reviewer', 'Anonymous')}")
            st.write(f"**Summary:** {metadata.get('summary', 'N/A')}")
        
        elif source['type'] == 'policy':
            st.write(f"**Document:** {metadata.get('title', 'N/A')}")


def main():
    # Header
    st.markdown('<p class="main-header">🛒 ShopAssist RAG</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">AI-Powered E-Commerce Product Assistant</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=ShopAssist", use_container_width=True)
        
        st.markdown("### About")
        st.info("""
        **ShopAssist RAG** helps you find products and answers questions using:
        - 50K+ product catalog
        - 100K+ customer reviews  
        - Store policies & FAQs
        """)
        
        st.markdown("### Settings")
        return_sources = st.checkbox("Show source documents", value=True)
        filter_type = st.selectbox(
            "Filter by type",
            ["All", "Products", "Reviews", "Policies"],
            index=0
        )
        
        st.markdown("### Example Queries")
        example_queries = {
            "Product": [
                "Best laptop for students under $800",
                "Gaming headphones with good reviews",
                "Affordable smartphones with great cameras"
            ],
            "Reviews": [
                "What do customers say about MacBook battery life?",
                "Common complaints about gaming laptops",
                "Is this brand reliable?"
            ],
            "Policy": [
                "What is your return policy?",
                "How long does shipping take?",
                "Do you offer warranty on electronics?"
            ]
        }
        
        for category, queries in example_queries.items():
            st.markdown(f"**{category} Questions:**")
            for query in queries:
                if st.button(query, key=query):
                    st.session_state.current_query = query
    
    # Main content
    try:
        pipeline = load_pipeline()
        
        # Stats
        stats = pipeline.get_stats()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Documents", f"{stats['total_documents']:,}")
        with col2:
            st.metric("Collection", stats['collection_name'])
        with col3:
            st.metric("Status", "🟢 Active")
        
        st.markdown("---")
        
        # Query input
        if 'current_query' not in st.session_state:
            st.session_state.current_query = ""
        
        query = st.text_input(
            "Ask me anything about products, reviews, or store policies:",
            value=st.session_state.current_query,
            placeholder="e.g., What's the best laptop for video editing under $1500?",
            key="query_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            search_button = st.button("🔍 Search", type="primary")
        with col2:
            if st.button("🗑️ Clear"):
                st.session_state.current_query = ""
                st.rerun()
        
        # Process query
        if search_button and query:
            with st.spinner("🤔 Thinking..."):
                # Map filter selection
                filter_map = {
                    "All": None,
                    "Products": "product",
                    "Reviews": "review",
                    "Policies": "policy"
                }
                
                # Query RAG pipeline
                result = pipeline.query(
                    query=query,
                    return_sources=return_sources,
                    filter_type=filter_map[filter_type]
                )
                
                # Display answer
                st.markdown("### 💬 Answer")
                st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)
                
                # Display sources
                if return_sources and result.get('sources'):
                    st.markdown("---")
                    st.markdown(f"### 📚 Sources ({result['num_sources']} documents)")
                    
                    for i, source in enumerate(result['sources']):
                        display_source(source, i)
        
        elif not query and search_button:
            st.warning("⚠️ Please enter a question first!")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure you've run `python scripts/build_vector_store.py` first!")


if __name__ == "__main__":
    main()