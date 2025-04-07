from elasticsearch_dsl.query import MultiMatch, Match
from .documents import StandardDocDocument
from django.core.paginator import Paginator
from django.shortcuts import render

def search(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    results = []

    if query:
        s = StandardDocDocument.search()

        # 숫자만 들어온 경우 code 필드로 검색
        if query.isdigit():
            s = s.query('match', code=query)
        else:
            s = s.query(
                MultiMatch(query=query, fields=['name', 'contents', 'name_en', 'contents_en'],
                           fuzziness='auto')
            )

        s = s.highlight_options(pre_tags='<span class="highlight">', post_tags='</span>')
        s = s.highlight('name', 'contents', 'name_en', 'contents_en')

        response = s[(int(page) - 1) * 10:int(page) * 10].execute()
        paginator = Paginator(response.hits, 10)
        results = paginator.get_page(page)

    return render(request, 'search_app/search.html', {
        'query': query,
        'results': results
    })
