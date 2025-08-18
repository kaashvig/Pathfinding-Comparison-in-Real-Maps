import streamlit as st
import pandas as pd
import folium
import time
import numpy as np
from main import PunePathfinder

# Page configuration
st.set_page_config(
    page_title="Pune Pathfinding Visualizer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for animations and visual appeal
st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        animation: fadeIn 1s ease-out;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .algorithm-progress {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    .success-message {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 1rem;
        animation: fadeIn 0.5s ease-out;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 0.5rem;
        animation: fadeIn 0.8s ease-out;
        transition: transform 0.3s ease;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .map-container {
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: fadeIn 1.2s ease-out;
    }
    
    .algorithm-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 0.5rem;
        animation: fadeIn 1s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .algorithm-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 2rem;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Animated Header
st.markdown("""
<div class="main-header">
    <h1> Pune Pathfinding Algorithm Visualizer</h1>
    <p>Compare BFS, Dijkstra, and A* algorithms on real road networks</p>
    <p>✨ Watch algorithms find optimal paths in real-time ✨</p>
</div>
""", unsafe_allow_html=True)

# Initialize pathfinder with loading animation
@st.cache_resource
def load_pathfinder():
    return PunePathfinder()

# Loading animation
with st.spinner('Loading Pune road network...'):
    try:
        pathfinder = load_pathfinder()
        time.sleep(0.5)  # Brief pause for effect
        st.markdown('<div class="success-message">Road network loaded successfully! Ready to compute paths.</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load network: {str(e)}")
        st.stop()

# Sidebar configuration
st.sidebar.markdown("## Path Configuration")

# Popular locations
popular_locations = [
    "Shaniwar Wada", "MIT World Peace University", "Pune Railway Station",
    "Koregaon Park", "Deccan Gymkhana", "Hadapsar", "Kothrud",
    "Viman Nagar", "Baner", "Wakad", "Phoenix MarketCity",
    "Pune Airport", "Camp", "FC Road", "MG Road", "Aundh",
    "Kalyani Nagar", "Hinjewadi"
]

# Location inputs with icons
with st.sidebar.container():
    st.markdown("### Select Route")
    col1, col2 = st.columns(2)
    with col1:
        start_location = st.selectbox(" Start", popular_locations, index=0)
    with col2:
        end_location = st.selectbox("🏁 Destination", popular_locations, index=2)

# Custom location inputs
with st.sidebar.expander(" Custom Locations"):
    custom_start = st.text_input("Custom Start", placeholder="Enter any Pune location")
    custom_end = st.text_input("Custom End", placeholder="Enter any Pune location")
    
    if custom_start:
        start_location = custom_start
    if custom_end:
        end_location = custom_end

# Algorithm information with animations
with st.sidebar.expander("Algorithm Information"):
    st.markdown("""
    🔴 **BFS**: Explores layer by layer (shortest hops)  
    🔵 **Dijkstra**: Finds shortest distance (guaranteed optimal)  
    🟢 **A***: Smart search with heuristic (fastest)
    """)

# Main action button with enhanced styling
if st.sidebar.button(" Calculate Optimal Paths", type="primary", use_container_width=True):
    if start_location != end_location:
        
        # Animated progress section
        st.markdown("""
        <div class="algorithm-progress">
            <h3>🔍 Computing Pathfinding Algorithms...</h3>
            <p>Analyzing road network and calculating optimal routes</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Multi-stage progress with realistic steps
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Stage 1: Geocoding
            status_text.text("🗺️ Geocoding locations...")
            for i in range(15):
                time.sleep(0.1)
                progress_bar.progress(i + 1)
            
            # Stage 2: Graph preparation
            status_text.text("Preparing road network graph...")
            for i in range(15, 35):
                time.sleep(0.08)
                progress_bar.progress(i + 1)
            
            # Stage 3: Running algorithms
            status_text.text("Running pathfinding algorithms...")
            for i in range(35, 85):
                time.sleep(0.05)
                progress_bar.progress(i + 1)
            
            # Stage 4: Visualization
            status_text.text(" Creating visualization...")
            for i in range(85, 100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
            
            status_text.text(" Path calculation complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()

        try:
            # Calculate paths
            with st.spinner("Processing algorithms..."):
                results, start_node, end_node = pathfinder.compare_algorithms(start_location, end_location)
            
            # Success animation
            st.balloons()
            
            # Results section with animations
            st.markdown("##  Algorithm Comparison Results")
            
            # Create enhanced results table with animations
            df_results = pd.DataFrame([
                {
                    'Algorithm': result['algorithm'],
                    'Distance (m)': f"{result['distance']:.1f}",
                    'Execution Time (s)': f"{result['execution_time']:.4f}",
                    'Nodes in Path': result['nodes_explored'],
                    'Status': 'Success' if result['path'] else ' Failed'
                }
                for result in results
            ])
            
            # Animated table appearance
            time.sleep(0.3)
            st.dataframe(df_results, use_container_width=True, hide_index=True)
            
            # Performance metrics with animated cards
            if all(result['path'] for result in results):
                st.markdown("## ⚡ Performance Analysis")
                
                fastest_algo = min(results, key=lambda x: x['execution_time'])['algorithm']
                shortest_path = min(results, key=lambda x: x['distance'])['algorithm']
                avg_time = sum(r['execution_time'] for r in results) / len(results)
                total_distance = sum(r['distance'] for r in results if r['path'])
                
                col1, col2, col3, col4 = st.columns(4)
                
                metrics_data = [
                    (" Fastest Algorithm", fastest_algo),
                    (" Shortest Path", shortest_path), 
                    (" Average Time", f"{avg_time:.4f}s"),
                    (" Total Distance", f"{total_distance:.0f}m")
                ]
                
                for i, (col, (label, value)) in enumerate(zip([col1, col2, col3, col4], metrics_data)):
                    time.sleep(0.2)  # Staggered animation
                    with col:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>{label}</h4>
                            <h2>{value}</h2>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Map visualization with container styling
            st.markdown("## 🗺️ Interactive Path Visualization")
            
            try:
                # Simulate map loading
                with st.spinner(" Rendering interactive map..."):
                    time.sleep(1)
                    map_obj = pathfinder.create_visualization_map(results, start_node, end_node)
                
                # Map container with styling
                st.markdown('<div class="map-container">', unsafe_allow_html=True)
                from streamlit_folium import folium_static
                folium_static(map_obj, width=1200, height=600)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Legend with animation
                time.sleep(0.5)
                st.markdown("""
                <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #667eea, #764ba2); 
                           color: white; border-radius: 0.5rem; margin-top: 1rem;">
                    <strong>Path Legend:</strong> 
                    🔴 BFS (Solid) | 🔵 Dijkstra (Dashed) | 🟢 A* (Dotted)
                </div>
                """, unsafe_allow_html=True)
                
            except ImportError:
                st.error("Please install: `pip install streamlit-folium`")
            
            # Algorithm details with enhanced cards
            st.markdown("## Algorithm Deep Dive")
            
            col1, col2, col3 = st.columns(3)
            
            algorithm_info = [
                ("🔴 BFS (Breadth-First Search)", "Unweighted", "Explores level by level", "Shortest path by hops", "High memory usage", "Small networks"),
                ("🔵 Dijkstra's Algorithm", "Weighted", "Priority queue with distances", "Shortest path by distance", "Medium memory usage", "Guaranteed optimal paths"),
                ("🟢 A* Algorithm", "Weighted + Heuristic", "Guided search with heuristic", "Optimal with good heuristic", "Medium memory usage", "Large graphs with targets")
            ]
            
            for i, (col, (title, type_info, approach, guarantee, memory, best_for)) in enumerate(zip([col1, col2, col3], algorithm_info)):
                time.sleep(0.3)  # Staggered animation
                with col:
                    st.markdown(f"""
                    <div class="algorithm-card">
                        <h4>{title}</h4>
                        <p><strong>Type:</strong> {type_info}</p>
                        <p><strong>Approach:</strong> {approach}</p>
                        <p><strong>Guarantee:</strong> {guarantee}</p>
                        <p><strong>Memory:</strong> {memory}</p>
                        <p><strong>Best for:</strong> {best_for}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Technical details
            with st.expander("🔧 Technical Implementation Details"):
                st.markdown("""
                ** Graph Representation:** OpenStreetMap road network via OSMnx  
                ** Edge Weights:** Physical distance in meters  
                ** Heuristic Function:** Haversine distance (great-circle)  
                ** Node Selection:** Nearest graph node to geocoded coordinates  
                ** Visualization:** Folium with distinct colored polylines per algorithm
                """)
        
        except Exception as e:
            st.error(f" Error occurred: {str(e)}")
            st.info("Try using predefined locations or check your spelling.")
    else:
        st.warning(" Please select different start and end locations.")

# Animated footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem; background: linear-gradient(45deg, #f093fb, #f5576c); 
           color: white; border-radius: 1rem; margin-top: 2rem;">
    <h3>PBL3 Project</h3>
    <p><strong>MIT World Peace University | TY CSE-CSF</strong></p>
    <p><em>Comparative Analysis of Pathfinding Algorithms on Real-World Road Networks</em></p>
    <p>Built with Streamlit, OSMnx, and Folium </p>
</div>
""", unsafe_allow_html=True)
