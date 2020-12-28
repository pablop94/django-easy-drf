from .core import Creator, TemplateHandler, FileHandler
from .drf_handlers import SerializersHandler, ViewsHandler, URLsHandler

    
def create_all(current_directory):
    creator = _get_creator(current_directory, SerializersHandler, ViewsHandler, URLsHandler)

    creator.create()

def create_serializers(current_directory):
    creator = _get_creator(current_directory, SerializersHandler)

    creator.create()

def create_views(current_directory):
    creator = _get_creator(current_directory, ViewsHandler)

    creator.create()

def create_urls(current_directory):
    creator = _get_creator(current_directory, URLsHandler)

    creator.create()
    

def _get_creator(directory, *args):
    template_handler = TemplateHandler(FileHandler())

    return Creator(directory, [klass(template_handler) for klass in args], template_handler)
