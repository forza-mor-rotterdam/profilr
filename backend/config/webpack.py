# in app.module
import os

import requests
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from webpack_loader.loader import WebpackLoader


class ExternalWebpackLoader(WebpackLoader):
    def load_assets(self):
        url = self.config["STATS_URL"]
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "done",
                "chunks": {
                    "app": [],
                    "js": {},
                },
                "assets": {},
            }

    def get_chunk_url(self, chunk_file):
        public_path = chunk_file.get("publicPath")
        if public_path:
            return f"{settings.PROJECT_URL}{public_path}"

        # Use os.path.normpath for Windows paths
        relpath = os.path.normpath(
            os.path.join(self.config["BUNDLE_DIR_NAME"], chunk_file["name"])
        )
        return staticfiles_storage.url(relpath)
