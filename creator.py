import ast
import astunparse

def create_serializers_and_views():
    with open('./models.py', 'r') as file:
        models_ast = ast.parse(file.read())


    serializers_ast = ast.parse("""
from rest_framework import serializers
from .models import *
        """)

    views_ast = ast.parse("""
from rest_framework import viewsets
from .serializers import *
from .models import *
        """)

    model_classes = [clss for clss in models_ast.body if clss.__class__ is ast.ClassDef]

    for mc in model_classes:
        class_fields = [field for field in mc.body if field.__class__ is ast.Assign]


        serializers_ast.body.append(ast.parse(f"""
class {mc.name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {mc.name}
        fields = ('id',{", ".join([f"'{field_name.targets[0].id}'" for field_name in class_fields])})
            """))

        views_ast.body.append(ast.parse(f"""
class {mc.name}ViewSet(viewsets.ModelViewSet):
    queryset = {mc.name}.objects.all()
    serializer_class = {mc.name}Serializer
            """))


    with open('./serializers.py', 'w') as wfile:
        wfile.write(astunparse.unparse(serializers_ast))

    with open('./views.py', 'w') as wfile:
        wfile.write(astunparse.unparse(views_ast))


if __name__ == '__main__':
    create_serializers_and_views()