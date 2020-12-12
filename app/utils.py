import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_html_components as html
from flask_login import current_user, login_required
from flask.helpers import get_root_path


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun=None, common_callbacks=None,
                     protect=False):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    assets = get_root_path(__name__) + f'/dash_apps{base_pathname.replace("-", "_")}assets/'
    print(assets)
    single_dashapp = dash.Dash(__name__,
                               server=app,
                               url_base_pathname=base_pathname,
                               assets_folder=assets,
                               meta_tags=[meta_viewport],
                               external_stylesheets=[dbc.themes.BOOTSTRAP])

    with app.app_context():
        single_dashapp.title = title
        single_dashapp.layout = layout
        if register_callbacks_fun:
            register_callbacks_fun(single_dashapp)
        # if common_callbacks:
        #     register_common_callbacks(single_dashapp)

    if protect:
        _protect_dashviews(single_dashapp)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_common_callbacks(dashapp):
    @dashapp.callback(
        Output('right-side-links', 'children'),
        [Input('none', 'children')],
        [State('right-side-links', 'children')]
    )
    def update_navbar(_, old_state_link):
        if current_user.is_authenticated:
            logout_link = dbc.NavItem(html.A('Logout', className="navbar-item", href='/logout',
                                             style={'color': 'white', 'paddingLeft': '10px'}))
            return [old_state_link[0], logout_link]
        else:
            return old_state_link
