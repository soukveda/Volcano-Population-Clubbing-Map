import folium
import pandas

# Retrieve contents from the .csv file
data = pandas.read_csv("Volcanoes.csv")

# Store specified data into variables
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "blue"

# Providing format for our popup
html1 = """
<h4>Volcano information:</h4>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

# Providing format for our clubbing popups
htmlclub = """
<h4>Club information:</h4>
Name: %s <br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">Click for more information</a>
"""
# Creating a folium map oject
map = folium.Map(location=[34.077600138961024, -118.26050448346554], zoom_start=10)#, tiles="Stamen Terrain")

# Creating an folium feature group object for our map
fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, name in zip(lat, lon, elev, name):
    # Applying html to the popup
    iframe = folium.IFrame(html=html1 % (name, name, str(el)), width=200, height=100)
    
    # Adding our new volcano markers to our map
    fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=7, popup=folium.Popup(iframe), fill_color=color_producer(el), color="grey", fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

# Creating a GeoJson object to open and read the given file
# folium will require a string, so you will need to read the file to pass to 'data' parameter
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor': 'yellow' if x['properties']['POP2005'] < 10000000 
else 'green' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# Applying htmlclub to these popups
iframeClub1 = folium.IFrame(html=htmlclub % ("143", "143 WORLDWIDE") , width=200, height=100)
iframeClub2 = folium.IFrame(html=htmlclub % ("Arena Ktown", "Arena Ktown"), width=200, height=100)

fgc = folium.FeatureGroup(name="Clubs")
# Adding new markers to our map
fgc.add_child(folium.Marker(location=[34.077600138961024, -118.26050448346554], popup=folium.Popup(iframeClub1), icon=folium.Icon(color='red')))
fgc.add_child(folium.Marker(location=[34.06195943458301, -118.29490961101035], popup=folium.Popup(iframeClub2), icon=folium.Icon(color='red')))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(fgc)

# Adding layer control functionality to our map
# Recommended to add this once all other map children are added
map.add_child(folium.LayerControl())
map.save("volcanoes-population-clubbing.html")
