import ast
import re
from .utils import get_viewset_name, get_serializer_name


class ImportHandler:
    def __init__(self, template_handler, file_name):
        self.template_handler = template_handler
        self.file_name = file_name

class ExistingImportHandler(ImportHandler):
    def is_relative_import(self, element, import_name):
        return element.__class__ is ast.ImportFrom and element.module == import_name and element.level == 1

    def get_import_template(self, model_classes):
        template = self.template_handler.get_file(self.file_name)
        for element in template.body:
            for key, transform in self.imports().items():
                if self.is_relative_import(element, key):
                    for model_class in model_classes:
                        element.names.append(ast.alias(transform(model_class.name), None))
        
        return template

    def imports(self):
        raise NotImplementedError('imports must be implemented by subclass')
    
class ExistingSerializerImportHandler(ExistingImportHandler):
    def imports(self):
        return {
            'models': lambda model_class_name: model_class_name
        }

class NonExistingSerializerImportHandler(ImportHandler):
    def get_import_template(self, model_classes):
        return self.template_handler.get_template(self.file_name, 
            model_classes=", ".join([model_class.name for model_class in model_classes]))

class ExistingViewImportHandler(ExistingImportHandler):
    def imports(self):
        return {
            'models': lambda model_class_name: model_class_name,
            'serializers': get_serializer_name
        }


class NonExistingViewImportHandler(ImportHandler):
    def get_import_template(self, model_classes):
        return self.template_handler.get_template(self.file_name, 
            model_classes=", ".join([model_class.name for model_class in model_classes]),
            serializer_classes=", ".join([get_serializer_name(model_class.name) for model_class in model_classes])
            )


class ExistingURLImportHandler(ExistingImportHandler):
    def imports(self):
        return {
            'models': lambda model_class_name: model_class_name,
            'views': get_viewset_name
        }


class NonExistingURLImportHandler(ImportHandler):
    def get_import_template(self, model_classes):
        return self.template_handler.get_template(self.file_name, viewset_names=", ".join([get_viewset_name(model_class.name) for model_class in model_classes]))
