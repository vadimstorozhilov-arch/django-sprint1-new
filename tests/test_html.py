import re

import pytest

from tests.conftest import try_get_url


@pytest.mark.parametrize(
    'url, slug', [
        ('/category/category_slug/', 'category_slug'),
        ('/category/another_slug/', 'another_slug'),
    ])
def test_category_page_contents(client, url, slug):
    response = try_get_url(client, url)
    msg_slug = '<slug>'
    msg_url = url.replace(slug, msg_slug)
    page_content = re.sub(r'\s+', ' ', response.content.decode())
    expected_text = f'Публикации в категории {slug}'
    assert expected_text in page_content, (
        f'Убедитесь, что на странице `{msg_url}` '
        f'отображается текст `Публикации в категории {msg_slug}`.'
    )
