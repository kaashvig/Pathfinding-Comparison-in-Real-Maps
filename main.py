import osmnx as ox
import networkx as nx
import folium
import time
from typing import Tuple, List, Dict, Optional
import math
import numpy as np

class PunePathfinder:
    def __init__(self, place_name: str = "Pune, Maharashtra, India"):
        """Initialize the pathfinder with Pune's road network"""
        print("Loading Pune road network...")
        ox.settings.use_cache = True
        ox.settings.log_console = False
        
        # Load Pune's road network
        self.G = ox.graph_from_place(place_name, network_type='drive', simplify=True)
        self.G = ox.add_edge_speeds(self.G)
        self.G = ox.add_edge_travel_times(self.G)
        
        print(f"Loaded graph with {len(self.G.nodes)} nodes and {len(self.G.edges)} edges")
        
        # Predefined coordinates for common Pune locations
        self.known_locations = {
            "Pune Railway Station": (18.528801, 73.874473),
            "Pune Junction": (18.528801, 73.874473),
            "Shaniwar Wada": (18.518889, 73.855833),
            "MIT World Peace University": (18.463889, 73.859167),
            "Phoenix MarketCity": (18.561111, 73.914444),
            "Koregaon Park": (18.539722, 73.888889),
            "Deccan Gymkhana": (18.518056, 73.850833),
            "Hadapsar": (18.508333, 73.926667),
            "Kothrud": (18.507500, 73.824167),
            "Viman Nagar": (18.567778, 73.914722),
            "Baner": (18.559722, 73.779167),
            "Wakad": (18.597500, 73.765833),
            "Pune Airport": (18.582778, 73.919722),
            "Camp": (18.518056, 73.878889),
            "FC Road": (18.518333, 73.840833),
            "MG Road": (18.518611, 73.852778),
            "Aundh": (18.554722, 73.807500),
            "Kalyani Nagar": (18.544444, 73.906667),
            "Hinjewadi": (18.591667, 73.738889)
        }
        
    def geocode_location(self, location_name: str) -> Tuple[float, float]:
        """Geocode a location name to lat, lon coordinates"""
        if location_name in self.known_locations:
            return self.known_locations[location_name]
        
        geocode_queries = [
            f"{location_name}, Pune, Maharashtra, India",
            f"{location_name}, Pune",
            f"{location_name} Pune Maharashtra",
            location_name
        ]
        
        for query in geocode_queries:
            try:
                gdf = ox.geocode_to_gdf(query)
                if not gdf.empty:
                    point = gdf.geometry.iloc[0].centroid
                    return point.y, point.x
            except:
                continue
                
        raise ValueError(f"Could not geocode location: {location_name}")
    
    def get_nearest_node(self, lat: float, lon: float) -> int:
        """Get the nearest node in the graph to given coordinates"""
        return ox.distance.nearest_nodes(self.G, lon, lat)
    
    def haversine_distance(self, node1: int, node2: int) -> float:
        """Calculate haversine distance between two nodes"""
        lat1, lon1 = self.G.nodes[node1]['y'], self.G.nodes[node1]['x']
        lat2, lon2 = self.G.nodes[node2]['y'], self.G.nodes[node2]['x']
        
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def bfs_pathfinding(self, start_node: int, end_node: int) -> Dict:
        """Breadth-First Search pathfinding (unweighted)"""
        start_time = time.time()
        
        try:
            path = nx.shortest_path(self.G, start_node, end_node)
            
            total_distance = 0
            for i in range(len(path) - 1):
                edge_data = self.G.get_edge_data(path[i], path[i + 1])
                if edge_data:
                    edge_length = min(edge_data.values(), key=lambda x: x.get('length', float('inf')))
                    total_distance += edge_length.get('length', 0)
            
            execution_time = time.time() - start_time
            
            return {
                'algorithm': 'BFS',
                'path': path,
                'distance': total_distance,
                'execution_time': execution_time,
                'nodes_explored': len(path)
            }
        except nx.NetworkXNoPath:
            return {
                'algorithm': 'BFS', 
                'path': [], 
                'distance': float('inf'), 
                'execution_time': time.time() - start_time, 
                'nodes_explored': 0
            }
    
    def dijkstra_pathfinding(self, start_node: int, end_node: int) -> Dict:
        """Dijkstra's algorithm pathfinding (weighted)"""
        start_time = time.time()
        
        try:
            path = nx.shortest_path(self.G, start_node, end_node, weight='length')
            total_distance = nx.shortest_path_length(self.G, start_node, end_node, weight='length')
            
            execution_time = time.time() - start_time
            
            return {
                'algorithm': 'Dijkstra',
                'path': path,
                'distance': total_distance,
                'execution_time': execution_time,
                'nodes_explored': len(path)
            }
        except nx.NetworkXNoPath:
            return {
                'algorithm': 'Dijkstra', 
                'path': [], 
                'distance': float('inf'), 
                'execution_time': time.time() - start_time, 
                'nodes_explored': 0
            }
    
    def astar_pathfinding(self, start_node: int, end_node: int) -> Dict:
        """A* algorithm pathfinding with haversine heuristic"""
        start_time = time.time()
        
        def heuristic(node1, node2):
            return self.haversine_distance(node1, node2)
        
        try:
            path = nx.astar_path(self.G, start_node, end_node, heuristic=heuristic, weight='length')
            
            total_distance = 0
            for i in range(len(path) - 1):
                edge_data = self.G.get_edge_data(path[i], path[i + 1])
                if edge_data:
                    edge_length = min(edge_data.values(), key=lambda x: x.get('length', float('inf')))
                    total_distance += edge_length.get('length', 0)
            
            execution_time = time.time() - start_time
            
            return {
                'algorithm': 'A*',
                'path': path,
                'distance': total_distance,
                'execution_time': execution_time,
                'nodes_explored': len(path)
            }
        except nx.NetworkXNoPath:
            return {
                'algorithm': 'A*', 
                'path': [], 
                'distance': float('inf'), 
                'execution_time': time.time() - start_time, 
                'nodes_explored': 0
            }
    
    def compare_algorithms(self, start_location: str, end_location: str) -> List[Dict]:
        """Compare all three algorithms"""
        start_lat, start_lon = self.geocode_location(start_location)
        end_lat, end_lon = self.geocode_location(end_location)
        
        start_node = self.get_nearest_node(start_lat, start_lon)
        end_node = self.get_nearest_node(end_lat, end_lon)
        
        print(f"Start: {start_location} -> Node {start_node}")
        print(f"End: {end_location} -> Node {end_node}")
        
        results = []
        results.append(self.bfs_pathfinding(start_node, end_node))
        results.append(self.dijkstra_pathfinding(start_node, end_node))
        results.append(self.astar_pathfinding(start_node, end_node))
        
        return results, start_node, end_node

    def create_visualization_map(self, results: List[Dict], start_node: int, end_node: int) -> folium.Map:
        """Create a Folium map with all three paths clearly visible using different styles"""
        # Get center point
        start_lat, start_lon = self.G.nodes[start_node]['y'], self.G.nodes[start_node]['x']
        end_lat, end_lon = self.G.nodes[end_node]['y'], self.G.nodes[end_node]['x']
        center_lat = (start_lat + end_lat) / 2
        center_lon = (start_lon + end_lon) / 2

        # Create map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

        # IMPROVED VISIBILITY: Much more distinct and visible styles
        path_styles = {
            'BFS': {
                'color': 'red', 
                'weight': 8,      # Much thicker line
                'opacity': 0.95,  # Almost fully opaque
                'dash_array': None  # Solid line
            },
            'Dijkstra': {
                'color': 'lightblue', 
                'weight': 8,      # Much thicker line
                'opacity': 0.8,  # Almost fully opaque
                'dash_array': '15,10'  # Long dashes with bigger gaps
            },
            'A*': {
                'color': 'limegreen',  # Brighter green color
                'weight': 7,      # Thick line but slightly thinner
                'opacity': 0.95,  # Almost fully opaque
                'dash_array': '5,8'   # Short dashes with bigger gaps
            }
        }

        # Draw paths in specific order to ensure visibility
        drawing_order = ['BFS', 'A*', 'Dijkstra']

        for algorithm_name in drawing_order:
            for result in results:
                if result['algorithm'] == algorithm_name and result['path']:
                    path_coords = []
                    for node in result['path']:
                        lat, lon = self.G.nodes[node]['y'], self.G.nodes[node]['x']
                        path_coords.append([lat, lon])

                    style = path_styles[result['algorithm']]

                    folium.PolyLine(
                        locations=path_coords,
                        color=style['color'],
                        weight=style['weight'],
                        opacity=style['opacity'],
                        dash_array=style['dash_array'],
                        popup=f"{result['algorithm']}: {result['distance']:.0f}m in {result['execution_time']:.4f}s"
                    ).add_to(m)

        # Add start and end markers
        folium.Marker(
            [start_lat, start_lon],
            popup="Start",
            icon=folium.Icon(color='green', icon='play')
        ).add_to(m)

        folium.Marker(
            [end_lat, end_lon],
            popup="End",
            icon=folium.Icon(color='red', icon='stop')
        ).add_to(m)

        # Enhanced legend with clearer descriptions and better visibility
        legend_html = """
        <div style="position: fixed; bottom: 50px; left: 50px; width: 320px; height: 200px; 
                    background-color: white; border: 3px solid grey; z-index: 9999; 
                    font-size: 15px; padding: 18px; border-radius: 10px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
        <p><b>🗺️ Pathfinding Algorithms</b></p>
        <p><span style="color: red; font-size: 22px; font-weight: bold;">━━━━━━━━</span> BFS (Red Solid)</p>
        <p><span style="color: blue; font-size: 22px; font-weight: bold;">━ ━ ━ ━ ━</span> Dijkstra (Blue Dashed)</p>
        <p><span style="color: limegreen; font-size: 22px; font-weight: bold;">• • • • • •</span> A* (Green Dotted)</p>
        <p style="font-size: 12px; color: #666; margin-top: 10px;">
        All paths show optimal routes with different algorithms
        </p>
        </div>
        """

        m.get_root().html.add_child(folium.Element(legend_html))

        return m
