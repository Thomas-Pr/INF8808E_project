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
    'color_way': ["#006233","#0011bb","#ff0000","#43A1D5"],
    'label_font_size': 14,
    'label_background_color': '#ffffff',
    'colorscale': 'RdBu'
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

            colorway=THEME['color_way'],
            colorscale={'sequential':THEME['colorscale']}
        )
    )


def set_default_theme():
    '''
        Sets the default theme to be a combination of the
        'plotly_white' theme and our custom theme.
    '''
    pio.templates.default = 'plotly_white+custom_theme'


'''
    Provides the templates for the tooltips.
'''

def add_template_line(name, value):
    '''
        Creates a template line for a label

        The label is followed by its corresponding
        value, separated by a colon
    '''
    temp_line = f"<b> {name}"
    temp_line += f":</b><span> {value}"
    temp_line += "</span><br>"
    # temp_line = f"<b style='font-family:{THEME['accent_font_family']}> {name}"
    # temp_line += f":</b><span style='font-family:{THEME['font_family']}'> {value}"
    # temp_line += "</span><br>"
    return temp_line
