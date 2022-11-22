# in app.module
import requests
from webpack_loader.loader import WebpackLoader

class ExternalWebpackLoader(WebpackLoader):

  def load_assets(self):
    url = self.config['STATS_URL']
    response = requests.get(url)   
    response.raise_for_status() 
    return response.json()