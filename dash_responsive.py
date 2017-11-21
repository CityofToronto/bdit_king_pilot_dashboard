'''Patch dash.Dash to enable adding meta tag to <head>'''

import dash

class DashResponsive(dash.Dash):
    """Patched version of dash.Dash to add a meta tag to <head>
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def index(self, *args, **kwargs):
        '''Overriding from https://github.com/plotly/dash/blob/master/dash/dash.py#L282
        '''
        scripts = self._generate_scripts_html()
        css = self._generate_css_dist_html()
        config = self._generate_config_html()
        title = getattr(self, 'title', 'King Street Transit Pilot: Vehicular Travel Time Monitoring')
        return ('''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
                <title>{}</title>
                {}
            </head>
            <body>
                <div id="react-entry-point">
                    <div class="_dash-loading">
                        Loading...
                    </div>
                </div>
            </body>
            <footer>
                {}
                {}
            </footer>
        </html>
        '''.format(title, css, config, scripts))
