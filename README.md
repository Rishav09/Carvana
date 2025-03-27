# Carvana Delivery Route Optimization Project

Vehicle route optimization is a critical problem for every logistics provider.  
This project demonstrates how to optimize delivery routes using `geopy` to calculate geographic distances and Google OR-Tools to solve the Vehicle Routing Problem (VRP).  
We use `folium` to build interactive maps that visualize optimized truck routes, and wrap the entire solution in a web application using `Streamlit`.

---

## Project Components and Workflow

### Data Loading and Preparation
- Load delivery location data from a CSV file into a pandas DataFrame.
- Compute a distance matrix between all locations using `geopy`’s geodesic distance.

### Vehicle Routing Problem (VRP) Solution
- Define the VRP, with constraints including:
  - A fixed depot (start and end point)
  - Limited truck capacity (e.g., 9 vehicles per truck)
- Solve the VRP using OR-Tools to minimize total route distance while satisfying all constraints.

### Route Extraction and Visualization
- Extract the optimized routes from the solver output.
- Visualize them on an interactive map using `folium`, with each truck’s route in a different color.

### Streamlit Integration
- Build an interactive web app using `Streamlit`.
- Users can:
  - Upload delivery location data
  - Choose the number of delivery trucks
  - Run the optimization
  - View updated routes on an interactive map

---

## Future Steps

- **Improve the user interface**  
  Refine the layout and style of the Streamlit app for a better user experience.

- **Incorporate real-time data**  
  Integrate APIs to use real-time traffic data and dynamic routing.

- **Add advanced delivery constraints**  
  Introduce time windows, driver hours, and vehicle-specific rules to handle more complex logistics scenarios.

- **Scale for large operations**  
  Optimize the algorithm to support hundreds of delivery points and dozens of vehicles.

---

## Technologies Used

- Python
- pandas, numpy
- geopy
- folium, streamlit, streamlit-folium
- ortools (Google Optimization Tools)

---

## Live Demo

You can try the app here:  
**👉 [https://caravana.streamlit.app/](https://caravana.streamlit.app/)**

---

## Running the App Locally

```bash
git clone https://github.com/rishav09/carvana-routing-app.git
cd carvana-routing-app
pip install -r requirements.txt
streamlit run app.py
