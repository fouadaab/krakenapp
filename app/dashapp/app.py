from fastapi import FastAPI
from pathlib import Path
import dash
import dash_bootstrap_components as dbc
from app.dashapp.layout import layout
from app.dashapp.callbacks import register_callbacks
from starlette.middleware.wsgi import WSGIMiddleware
from apis.v1.route_login import UserInDB


root_path = Path('.')

class DashWithUser(dash.Dash):
    def register_users(self, current_user: UserInDB):
        self.current_user = current_user
    def get_current_user(self):
        if self.current_user:
            return self.current_user[-1]

def mount_dash(app: FastAPI, users=None) -> None:
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = DashWithUser(
        __name__,
        requests_pathname_prefix='/dash/',
        assets_folder= root_path / 'dashapp/assets',
        meta_tags=[meta_viewport],
        external_stylesheets=[dbc.themes.CERULEAN],
        prevent_initial_callbacks=False,
    )

    dashapp.title = "Kraken Dashapp"
    dashapp.layout = layout

    # Capture latest user creds for dashapp
    dashapp.register_users(users)

    register_callbacks(app, dashapp)

    app.mount("/dash", WSGIMiddleware(dashapp.server))