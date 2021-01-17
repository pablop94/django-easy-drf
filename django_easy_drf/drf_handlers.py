import ast
import os
from .import_handlers import *
from .utils import get_viewset_name, get_serializer_name



class DRFHandler:
    def __init__(self, template_handler):
        super().__init__()
        self.template_handler = template_handler

    @property
    def code(self):
        raise NotImplementedError('code must be implemented by subclass')

    @property
    def result_name(self):
        raise NotImplementedError('result_name must be implemented by subclass')
    
    def handle(self, template, model_class):
        raise NotImplementedError('handle must be implemented by subclass')

    def get_import_handler(self):
        raise NotImplementedError('get_import_handler must be implemented by subclass')

    def get_import_template(self, model_classes):
        return self.get_import_handler().get_import_template(model_classes)


class SerializersHandler(DRFHandler):
    @property
    def code(self):
        return 'serializers'

    @property
    def result_name(self):
        return 'serializers.py'

    def get_import_handler(self):
        if os.path.exists(self.result_name):
            return ExistingSerializerImportHandler(self.template_handler, self.result_name)
        return NonExistingSerializerImportHandler(self.template_handler, self.code)

    def handle(self, template, model_class):
        class_fields = [field for field in model_class.body if field.__class__ is ast.Assign]

        template.body.append(self.template_handler.get_template('serializer', 
            model_class_name=model_class.name, 
            serializer_class_name=get_serializer_name(model_class.name),
            field_names=", ".join([f"'{field_name.targets[0].id}'" for field_name in class_fields])))


class ViewsHandler(DRFHandler):
    @property
    def code(self):
        return 'views'

    @property
    def result_name(self):
        return 'views.py'

    def get_import_handler(self):
        if os.path.exists(self.result_name):
            return ExistingViewImportHandler(self.template_handler, self.result_name)
        return NonExistingViewImportHandler(self.template_handler, self.code)

    def handle(self, template, model_class):
        template.body.append(self.template_handler.get_template('viewset', 
        viewset_name=get_viewset_name(model_class.name),
        serializer_class_name=get_serializer_name(model_class.name),
        model_class_name=model_class.name))


class URLsHandler(DRFHandler):
    @property
    def code(self):
        return 'urls'

    @property
    def result_name(self):
        return 'urls.py'

    def get_import_handler(self):
        if os.path.exists(self.result_name):
            return ExistingURLImportHandler(self.template_handler, self.result_name)
        return NonExistingURLImportHandler(self.template_handler, self.code)

    def handle(self, template, model_class):
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        mc_name_snake = pattern.sub('-', model_class.name).lower()
        template.body.insert(len(template.body)-1, self.template_handler.get_template('url', 
            viewset_name=get_viewset_name(model_class.name), 
            model_class_name_snake=mc_name_snake))
