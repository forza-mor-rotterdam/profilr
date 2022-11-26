# in app.module
import requests
from webpack_loader.loader import WebpackLoader

class ExternalWebpackLoader(WebpackLoader):

  def load_assets(self):
    url = self.config['STATS_URL']
    response = requests.get(url)   
    # response.raise_for_status() 
    if response.status_code == 200:
      return response.json()
    else:
      return {
        "status": "done",
        "chunks": {
          "app": [],
          "js": {},
        },
        "assets": {}
      }