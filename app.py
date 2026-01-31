import streamlit as st
import recommender

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Qulu",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS - The "Qulu" Theme
st.markdown("""
<style>
    /* RESET & LAYOUT */
    .stApp {
        background-color: #141414; /* Netflix/Hulu Dark Background */
        color: #ffffff;
    }
    
    /* Remove standard Streamlit top padding to simulate app-like feel */
    .block-container {
        padding-top: 20px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        max-width: 100% !important;
    }
    
    /* Hide Default Header/Footer if possible to clean up UI */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* TYPOGRAPHY */
    h1, h2, h3, h4, p, div {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* BRANDING: QULU Logo */
    .brand-logo {
        font-size: 2.5rem;
        font-weight: 900;
        color: #e50914; /* Netflix Red or use #1ce783 for Hulu Green. Using Red for high contrast/Netflix feel */
        letter-spacing: -1px;
        margin-bottom: 20px;
        text-transform: uppercase;
        display: inline-block;
    }

    /* SEARCH BAR STYLING */
    /* Target the stSelectbox widget */
    .stSelectbox > div > div {
        background-color: #333333;
        color: white;
        border: 1px solid #444;
        border-radius: 4px;
    }
    .stSelectbox div[data-baseweb="select"] {
        color: white;
        background-color: #333333;
    }

    /* BUTTON STYLING - "RECOMMEND" */
    .stButton > button {
        background-color: white;
        color: black;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        font-size: 1rem;
        padding: 0.6rem 2rem;
        transition: all 0.2s ease;
        text-transform: uppercase;
    }
    .stButton > button:hover {
        background-color: #e6e6e6; /* Slight dim on hover */
        transform: scale(1.02);
    }

    /* HORIZONTAL SCROLL SHELF (The Core Requirement) */
    .shelf-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e5e5e5;
        margin-top: 40px;
        margin-bottom: 15px;
        padding-left: 10px; /* Align with scroll start */
    }

    .shelf-container {
        display: flex;
        overflow-x: auto;
        padding: 20px 10px; /* Space for shadow and hover scale */
        gap: 15px;
        scroll-behavior: smooth;
        /* Hide scrollbar for cleaner look (works in Chrome/Safari/Edge) */
        scrollbar-width: none;  /* Firefox */
        -ms-overflow-style: none;  /* IE 10+ */
    }
    .shelf-container::-webkit-scrollbar { 
        display: none;  /* Chrome/Safari */
    }

    /* MOVIE CARD IN SHELF */
    .movie-card {
        flex: 0 0 auto; /* Don't shrink */
        width: 200px;   /* Fixed width for consistency */
        transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        cursor: pointer;
    }

    .movie-card:hover {
        transform: scale(1.08); /* Distinct "pop" effect */
        z-index: 10;
    }

    .movie-poster {
        width: 100%;
        aspect-ratio: 2/3; /* Enforce standard poster ratio */
        object-fit: cover;
        border-radius: 6px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    .movie-title {
        margin-top: 10px;
        font-size: 0.9rem;
        color: #b3b3b3;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        text-align: center;
        font-weight: 500;
    }

</style>
""", unsafe_allow_html=True)

# 3. Header / Branding
st.markdown('<div class="brand-logo">QULU</div>', unsafe_allow_html=True)

# 4. Search Area
# Using a "Form" like structure or helper callbacks for better state management
if 'current_movie' not in st.session_state:
    st.session_state.current_movie = None

def on_play_click():
    st.session_state.current_movie = st.session_state.search_selection

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.selectbox(
        "Search",
        recommender.titles,
        index=None,
        label_visibility="collapsed",
        placeholder="Search for a title...",
        key="search_selection"
    )

with col2:
    st.button("PLAY", use_container_width=True, on_click=on_play_click)

# 5. Recommendation Display Logic
if st.session_state.current_movie:
    movie_to_search = st.session_state.current_movie
    
    # Get Recommendations
    # Wrap in try-except to prevent app crash if logic fails
    try:
        recommendations = recommender.recommend(movie_to_search)
    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")
        recommendations = []

    if recommendations:
        # Display - Horizontal Scroll Shelf
        st.markdown(f'<div class="shelf-title">Because you watched "{movie_to_search}"</div>', unsafe_allow_html=True)
        
        # Build HTML for the shelf
        html_cards = ""
        for title, poster in recommendations:
            poster_src = poster if poster else "https://via.placeholder.com/200x300/111/888?text=No+Poster"
            
            html_cards += f"""<div class="movie-card">
    <img src="{poster_src}" class="movie-poster" alt="{title}">
    <div class="movie-title">{title}</div>
</div>"""
            
        render_shelf = f"""<div class="shelf-container">
    {html_cards}
</div>"""
        
        st.markdown(render_shelf, unsafe_allow_html=True)
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
    else:
        st.warning(f"No recommendations found for '{movie_to_search}'. Try another movie.")
    
else:
    # Landing State
    st.markdown('<div class="shelf-title">Start Watching</div>', unsafe_allow_html=True)
    st.info("Select a movie and press PLAY to see recommendations.")
