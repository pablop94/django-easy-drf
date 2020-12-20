import ast
import astunparse

def create_serializers_and_views():
    with open('./models.py', 'r') as file:
        models_ast = ast.parse(file.read())


    serializers_ast = _read_template('serializers')
    views_ast = _read_template('views')

    model_classes = [clss for clss in models_ast.body if clss.__class__ is ast.ClassDef]

    for mc in model_classes:
        class_fields = [field for field in mc.body if field.__class__ is ast.Assign]

        serializers_ast.body.append(_read_template('serializer', model_class_name=mc.name, 
            field_names=", ".join([f"'{field_name.targets[0].id}'" for field_name in class_fields])))

        views_ast.body.append(_read_template('viewset', model_class_name=mc.name))

    _write_result('./serializers.py', serializers_ast)
    _write_result('./views.py', views_ast)

def _read_template(template_name, **kwargs):
    with open(f'./templates/{template_name}', 'r') as template:
        return ast.parse(template.read().format(**kwargs))

def _write_result(result_file_name, ast_name):
    with open(result_file_name, 'w') as wfile:
        wfile.write(astunparse.unparse(ast_name)) 

if __name__ == '__main__':
    create_serializers_and_views()