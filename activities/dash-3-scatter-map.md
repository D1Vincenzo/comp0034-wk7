# 3. Scatter Mapbox

| Activity                            | Chart type                       | Data access method       | Chart library |
|:------------------------------------|:---------------------------------|:-------------------------|:--------------|
| [Activity 3](dash-3-scatter-map.md) | Scatter Mapbox, map with markers | pandas / SQLite database | Plotly Go     |

Please create the database first by running the code in `paralympics_dash/create_db_dash.py` as this will create a
version of the database that includes the latitude/longitude data. The database will be created within the
paralympics_dash directory.

You need to have the latitude and longitude of each event. These have been added to the SQLite database in a locations
table.

In week 2 we looked at creating a database using SQLite. One method is to use the sqlite3 library to create a database
connection and create a cursor to execute queries. The following code uses pandas to read from a SQLite database.

```python
paralympic_db = Path(__file__).parent.joinpath("paralympics_dash.sqlite")


def scatter_geo():
    # create database connection
    connection = sqlite3.connect(paralympic_db)

    # define the sql query
    sql = '''
        SELECT event.id, event.host, event.year, location.lat, location.lon
        FROM event
        JOIN location ON event.host = location.city 
        '''

    df_locs = pd.read_sql(sql=sql, con=connection, index_col=None)
    # The lat and lon are stored as string but need to be floats for the scatter_geo
    df_locs['lon'] = df_locs['lon'].astype(float)
    df_locs['lat'] = df_locs['lat'].astype(float)
    # Adds a new column that concatenates the city and year e.g. Barcelona 2012
    df_locs['name'] = df_locs['host'] + ' ' + df_locs['year'].astype(str)

    fig = px.scatter_geo(df_locs,
                         lat=df_locs.lat,
                         lon=df_locs.lon,
                         hover_name=df_locs.name,
                         title="Where have the paralympics been held?",
                         )
    return fig 
```

In paralympics_dash.py add code to create the figure using the function above, e.g.

```python
from figures import scatter_geo

# Create the scatter map
map = scatter_geo()
```

In the layout for row 3 add the dcc.Graph() and remove the placeholder image, e.g.

```python
row_four = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="map", figure=map)
        # html.Img(src=app.get_asset_url('map-placeholder.png'), className="img-fluid"),
    ], width=8),
    dbc.Col(children=[
        card,
    ], width=4),
], align="start")
```

Run the app if not already running. You should see a map of the world with small dots for each event. When you hover on
a dot it will show the city and year.

There are options for styling the markers, though this requires some Plotly Go syntax. Refer to the [Plotly maps
documentation](https://plotly.com/python/scatter-plots-on-maps/) if you want to try to change the marker styles.
