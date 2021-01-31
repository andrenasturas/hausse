import logging
from hausse.plugins.layout.handlebars import Handlebars

LAYOUTS = {
    "handlebars": Handlebars
}

# TODO: Merge with LayoutPlugin and make it a metaclass
def Layouts(engine: str = "handlebars", *args, **kwargs):
    plugin = LAYOUTS.get(engine.lower())

    if plugin is None:
        logging.error(f"Engine {engine} not in available layout engines : {', '.join(list(LAYOUTS.keys()))}")
    
    else:
        return plugin(*args, **kwargs)