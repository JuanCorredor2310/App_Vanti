import dash
import dash_html_components as html
from dash.dependencies import Input, Output

# Load the image
ruta = r'C:\\Users\\default.LAPTOP-BMGM3VDA\\Downloads\\plantilla.png'

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Img(id='image', src='file://' + ruta, style={'width': '100%', 'height': '100vh'})
], style={'margin': 0, 'padding': 0, 'overflow': 'hidden'})

if __name__ == '__main__':
    app.run_server()