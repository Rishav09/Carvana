import streamlit as st
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import folium
from streamlit_folium import st_folium

import streamlit as st
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import folium
from streamlit_folium import st_folium
import streamlit as st

st.sidebar.title("Navigation")
st.sidebar.markdown("Use the options below to interact with the app.")
num_vehicles = st.sidebar.slider("Select number of trucks", 1, 5, 3)

import pandas as pd

# Load the delivery locations from a CSV file
locations = pd.read_csv("carvana_delivery_locations.csv")

def compute_distance_matrix(locations):
    num_locations = len(locations)
    distance_matrix = np.zeros((num_locations, num_locations))
    for i in range(num_locations):
        for j in range(num_locations):
            coord1 = (locations.iloc[i]['lat'], locations.iloc[i]['lng'])
            coord2 = (locations.iloc[j]['lat'], locations.iloc[j]['lng'])
            distance_matrix[i][j] = geodesic(coord1, coord2).km
    return (distance_matrix * 1000).astype(int)

distance_matrix = compute_distance_matrix(locations)

def solve_vrp(locations, distance_matrix, num_vehicles=3, depot_index=0):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot_index)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Capacities and demands
    vehicle_capacities = [9] * num_vehicles
    demands = [0] + [1] * (len(locations) - 1)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0, vehicle_capacities, True, 'Capacity')

    # Solve
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    solution = routing.SolveWithParameters(search_params)

    routes = []
    if solution:
        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route.append(node_index)
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
            routes.append(route)
    return routes

def plot_routes(locations, routes):
    depot_lat = locations.iloc[0]['lat']
    depot_lng = locations.iloc[0]['lng']
    m = folium.Map(location=[depot_lat, depot_lng], zoom_start=12)
    colors = ['red', 'blue', 'green', 'purple', 'orange']

    folium.Marker(
        [depot_lat, depot_lng],
        popup="Depot",
        icon=folium.Icon(color='black', icon='home', prefix='fa')
    ).add_to(m)

    for i, route in enumerate(routes):
        route_coords = []
        color = colors[i % len(colors)]
        for idx in route:
            lat, lng = locations.iloc[idx][['lat', 'lng']]
            route_coords.append((lat, lng))
            if idx != 0:
                folium.CircleMarker(
                    location=(lat, lng),
                    radius=5,
                    color=color,
                    fill=True,
                    fill_opacity=0.8,
                    popup=locations.iloc[idx]['location_id']
                ).add_to(m)
        folium.PolyLine(route_coords, color=color, weight=3).add_to(m)
    return m

st.title("Carvana Delivery Route Optimizer")
num_vehicles = st.slider("Select number of trucks", 1, 5, 3)
routes = solve_vrp(locations, distance_matrix, num_vehicles=num_vehicles)

if routes:
    st.success("Optimized routes calculated!")
    map_ = plot_routes(locations, routes)
    st_folium(map_, width=700, height=500)
else:
    st.error("No solution found.")
