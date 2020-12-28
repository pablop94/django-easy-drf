#!/usr/bin/env python3

import os
import ast
import astunparse
import re


def create_all(current_directory):
    model_classes = _get_model_classes(current_directory)
    _create_serializers_file(model_classes, current_directory)
    _create_views_file(model_classes, current_directory)
    _create_urls_file(model_classes, current_directory)


def create_serializers(current_directory):
    model_classes = _get_model_classes(current_directory)
    _create_serializers_file(model_classes, current_directory)


def create_views(current_directory):
    model_classes = _get_model_classes(current_directory)
    _create_views_file(model_classes, current_directory)

def create_urls(current_directory):
    model_classes = _get_model_classes(current_directory)
    _create_urls_file(model_classes, current_directory)


def _create_serializers_file(model_classes, directory):
    serializers_ast = _read_template('serializers')

    for model_class in model_classes:
        _add_serializer_class(serializers_ast, model_class)

    _write_result(os.path.join(directory, 'serializers.py'), serializers_ast)


def _create_views_file(model_classes, directory):
    views_ast = _read_template('views')

    for model_class in model_classes:
        _add_view_class(views_ast, model_class)

    _write_result(os.path.join(directory, 'views.py'), views_ast)


def _create_urls_file(model_classes, directory):
    urls_ast = _read_template('urls')

    for model_class in model_classes:
        _add_url_route(urls_ast, model_class)

    _write_result(os.path.join(directory, 'urls.py'), urls_ast)


def _add_serializer_class(serializers_ast, model_class):
    class_fields = [field for field in model_class.body if field.__class__ is ast.Assign]

    serializers_ast.body.append(_read_template('serializer', model_class_name=model_class.name, 
        field_names=", ".join([f"'{field_name.targets[0].id}'" for field_name in class_fields])))

def _add_view_class(views_ast, model_class):
    views_ast.body.append(_read_template('viewset', model_class_name=model_class.name))

def _add_url_route(urls_ast, model_class):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    mc_name_snake = pattern.sub('-', model_class.name).lower()
    urls_ast.body.insert(len(urls_ast.body)-1, _read_template('url', model_class_name=model_class.name, model_class_name_snake=mc_name_snake))



def _get_model_classes(directory):
    with open(os.path.join(directory, 'models.py'), 'r') as file:
        models_ast = ast.parse(file.read())

    return [clss for clss in models_ast.body if clss.__class__ is ast.ClassDef]


def _read_template(template_name, **kwargs):
    script_folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_folder, f'templates/{template_name}'), 'r') as template:
        return ast.parse(template.read().format(**kwargs))

def _write_result(result_file_name, ast_name):
    with open(result_file_name, 'w') as wfile:
        wfile.write(astunparse.unparse(ast_name)) 

