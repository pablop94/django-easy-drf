import ast
import re

def get_viewset_name(model_class_name):
    return f'{model_class_name}ViewSet'

def get_serializer_name(model_class_name):
    return f'{model_class_name}Serializer'

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

    def get_import_template(self, *args):
        return self.template_handler.get_template(self.code)


class SerializersHandler(DRFHandler):
    @property
    def code(self):
        return 'serializers'

    @property
    def result_name(self):
        return 'serializers.py'

    def get_import_template(self, model_classes):
        return self.template_handler.get_template(self.code, 
            model_classes=", ".join([model_class.name for model_class in model_classes]))

    def handle(self, template, model_class):
        class_fields = [field for field in model_class.body if field.__class__ is ast.Assign]

        template.body.append(self.template_handler.get_template('serializer', model_class_name=model_class.name, 
            field_names=", ".join([f"'{field_name.targets[0].id}'" for field_name in class_fields])))


class ViewsHandler(DRFHandler):
    @property
    def code(self):
        return 'views'

    @property
    def result_name(self):
        return 'views.py'

    def get_import_template(self, model_classes):
        return self.template_handler.get_template(self.code, 
            model_classes=", ".join([model_class.name for model_class in model_classes]),
            serializer_classes=", ".join([get_serializer_name(model_class.name) for model_class in model_classes])
            )

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

    def get_import_template(self, model_classes):
        return self.template_handler.get_template(self.code, viewset_names=", ".join([get_viewset_name(model_class.name) for model_class in model_classes]))

    def handle(self, template, model_class):
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        mc_name_snake = pattern.sub('-', model_class.name).lower()
        template.body.insert(len(template.body)-1, self.template_handler.get_template('url', 
            viewset_name=get_viewset_name(model_class.name), 
            model_class_name_snake=mc_name_snake))


