'''
    Contains the template to use in the data visualization.
'''
import plotly.graph_objects as go
import plotly.io as pio


THEME = {
    'background_color': '#ffffff',
    'font_family': 'Roboto',
    'accent_font_family': 'Roboto Slab',
    'dark_color': '#2A2B2E',
    'pale_color': '#DFD9E2',
    'colorway': ["#006233","#0011bb","#ff0000","#D5B048"],
    'label_font_size': 14,
    'label_background_color': '#ffffff',
    'colorscale': ["#ff0000","#ffffff","#006233"]
}


def create_custom_theme():
    '''
        Adds a new layout template to pio's templates.
    '''
    pio.templates['custom_theme'] = go.layout.Template(
        layout=go.Layout(
            font_color=THEME['dark_color'],
            font_family=THEME['font_family'],

            plot_bgcolor=THEME['background_color'],
            paper_bgcolor=THEME['background_color'],

            hoverlabel=dict(
                bgcolor=THEME['label_background_color'],
                font=dict(size = THEME['label_font_size'],
                            color = THEME['dark_color'])
            ),
            hovermode='closest',

            colorway=THEME['colorway'],
            colorscale={'sequential':THEME['colorscale']}
        )
    )


def set_default_theme():
    '''
        Sets the default theme to be a combination of the
        'plotly_white' theme and our custom theme.
    '''
    pio.templates.default = 'plotly_white+custom_theme'