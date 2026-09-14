import os
import re
from pathlib import Path


def test_project_folder_in_place(root_dir, project_dirname):
    manage_rpath = os.path.join(project_dirname, 'manage.py')
    manage_fpath = os.path.join(root_dir, manage_rpath)
    assert os.path.isfile(manage_fpath), (
        f'Не найден файл `{manage_rpath}`. '
        'Убедитесь, что структура проекта соответствует заданию.'
    )


def test_templates_use_url_tag(root_dir, project_dirname):
    templates_dir = Path(root_dir) / project_dirname / 'templates'
    assert templates_dir.is_dir(), (
        'Убедитесь, что шаблоны проекта находятся в директории '
        '`blogicum/templates/`.'
    )
    templates_content = '\n'.join(
        template.read_text(encoding='utf-8')
        for template in templates_dir.rglob('*.html')
    )
    for url_name in (
        'blog:index',
        'blog:post_detail',
        'blog:category_posts',
        'pages:about',
        'pages:rules',
    ):
        url_tag_pattern = re.compile(
            r'{%\s*url\s+[\'"]' + re.escape(url_name) + r'[\'"]'
        )
        assert re.search(url_tag_pattern, templates_content), (
            'Убедитесь, что для внутренних ссылок в шаблонах используется '
            f'тег `{{% url %}}` с именем маршрута `{url_name}`.'
        )
    hardcoded_links = re.findall(
        r'href=[\'"]/(?!static/)[^\'"]*[\'"]',
        templates_content,
    )
    assert not hardcoded_links, (
        'Убедитесь, что внутренние ссылки в шаблонах формируются через '
        'тег `{% url %}`, а не прописаны вручную.'
    )


def test_no_default_django_comments(root_dir, project_dirname):
    project_dir = Path(root_dir) / project_dirname
    default_comments = (
        'Create your views here.',
        'Create your models here.',
        'Register your models here.',
        'Create your tests here.',
    )
    for py_file in project_dir.rglob('*.py'):
        file_content = py_file.read_text(encoding='utf-8')
        assert not any(comment in file_content for comment in default_comments), (
            'Удалите стандартные комментарии Django из файлов проекта.'
        )
