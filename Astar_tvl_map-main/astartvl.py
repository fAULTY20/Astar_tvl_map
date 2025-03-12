import heapq
import folium
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Define graph with additional paths and corrected distances (in km)
graph = {
    'Palayamkottai': {'Nazareth': (30, 35), 'Nanguneri': (22, 28), 'Thalayuthu': (15, 20)},
    'Nazareth': {'Palayamkottai': (30, 35), 'Vallioor': (32, 38), 'Suviseshapuram': (18, 22), 'Eral': (25, 30)},
    'Nanguneri': {'Palayamkottai': (22, 28), 'Thalayuthu': (35, 40), 'Vallioor': (20, 25)},
    'Vallioor': {'Nazareth': (32, 38), 'Eral': (40, 45), 'Nanguneri': (20, 25)},
    'Thalayuthu': {'Nanguneri': (35, 40), 'Pettai': (18, 22), 'Palayamkottai': (15, 20)},
    'Eral': {'Vallioor': (40, 45), 'Seevalaperi': (30, 35), 'Nazareth': (25, 30)},
    'Pettai': {'Thalayuthu': (18, 22), 'Seevalaperi': (12, 15), 'Town': (20, 25)},
    'Seevalaperi': {'Eral': (30, 35), 'Pettai': (12, 15)},
    'Town': {'Palayamkottai': (5, 7), 'Sathankulam': (35, 40), 'Pettai': (20, 25)},
    'Sathankulam': {'Town': (35, 40), 'Desaiyanvilai': (10, 15), 'Nazareth': (28, 35)},
    'Desaiyanvilai': {'Sathankulam': (10, 15), 'Suviseshapuram': (12, 18)},
    'Suviseshapuram': {'Desaiyanvilai': (12, 18), 'Nazareth': (18, 22)}
}

# Define heuristic values (straight-line distance estimation)
heuristic = {
    'Palayamkottai': {'Seevalaperi': 40},
    'Nazareth': {'Seevalaperi': 35},
    'Nanguneri': {'Seevalaperi': 30},
    'Vallioor': {'Seevalaperi': 28},
    'Thalayuthu': {'Seevalaperi': 25},
    'Eral': {'Seevalaperi': 20},
    'Pettai': {'Seevalaperi': 12},
    'Seevalaperi': {'Seevalaperi': 0},
    'Town': {'Seevalaperi': 50},
    'Sathankulam': {'Seevalaperi': 45},
    'Desaiyanvilai': {'Seevalaperi': 38},
    'Suviseshapuram': {'Seevalaperi': 35}
}

# City coordinates
city_coords = {
    'Palayamkottai': (8.7051, 77.7388),
    'Nazareth': (8.5541, 77.8780),
    'Nanguneri': (8.4825, 77.6854),
    'Vallioor': (8.3823, 77.6142),
    'Thalayuthu': (8.7721, 77.6493),
    'Eral': (8.6201, 77.9200),
    'Pettai': (8.7392, 77.7125),
    'Seevalaperi': (8.7463, 77.6789),
    'Town': (8.7139, 77.7519),
    'Sathankulam': (8.4044, 77.9057),
    'Desaiyanvilai': (8.3698, 77.9262),
    'Suviseshapuram': (8.3201, 77.9500)
}

# A* Algorithm
def a_star(graph, heuristic, start, goal):
    pq = []
    heapq.heappush(pq, (0, start))
    g_cost = {city: float('inf') for city in graph}
    g_cost[start] = 0
    parent = {start: None}
    
    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            break
        
        for neighbor, (distance, _) in graph[current].items():
            new_g_cost = g_cost[current] + distance
            if new_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_g_cost
                f_cost = new_g_cost + heuristic[neighbor].get(goal, float('inf'))
                heapq.heappush(pq, (f_cost, neighbor))
                parent[neighbor] = current
    
    path = []
    city = goal
    while city is not None:
        path.append(city)
        city = parent[city]
    path.reverse()
    
    return path, g_cost[goal]

# Generate Map
def generate_map(start, goal, path):
    m = folium.Map(location=[8.6, 77.8], zoom_start=10)
    for city, coords in city_coords.items():
        folium.Marker(coords, popup=city, icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(city_coords[start], popup="Start", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(city_coords[goal], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
    path_coords = [city_coords[city] for city in path]
    folium.PolyLine(path_coords, color="blue", weight=4.5, opacity=0.7).add_to(m)
    m.save("tirunelveli_route_map.html")
    messagebox.showinfo("Map Saved", "Route Map has been saved as 'tirunelveli_route_map.html'. Open it in a browser.")

# GUI for city selection
def run_gui():
    def find_route():
        start = start_var.get()
        goal = goal_var.get()
        if start == goal:
            messagebox.showerror("Error", "Start and Destination cannot be the same!")
            return
        if start not in graph or goal not in graph:
            messagebox.showerror("Error", "Invalid City Selection!")
            return
        
        path, total_distance = a_star(graph, heuristic, start, goal)
        result_label.config(text=f"Optimal Path: {' -> '.join(path)}\nTotal Distance: {total_distance} km")
        generate_map(start, goal, path)

    root = tk.Tk()
    root.title("Tirunelveli A* Route Finder")
    
    ttk.Label(root, text="Select Starting City:").grid(row=0, column=0)
    start_var = tk.StringVar()
    start_dropdown = ttk.Combobox(root, textvariable=start_var, values=list(graph.keys()))
    start_dropdown.grid(row=0, column=1)
    
    ttk.Label(root, text="Select Destination City:").grid(row=1, column=0)
    goal_var = tk.StringVar()
    goal_dropdown = ttk.Combobox(root, textvariable=goal_var, values=list(graph.keys()))
    goal_dropdown.grid(row=1, column=1)
    
    find_button = ttk.Button(root, text="Find Route", command=find_route)
    find_button.grid(row=2, columnspan=2)
    
    result_label = ttk.Label(root, text="", foreground="blue")
    result_label.grid(row=3, columnspan=2)
    
    root.mainloop()

# Run the GUI
run_gui()
