from elasticsearch_dsl.query import MultiMatch
from .documents import StandardDocDocument
from django.core.paginator import Paginator
from django.shortcuts import render

def search(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    results = []

    if query:
        search_query = StandardDocDocument.search().query(
            MultiMatch(query=query, fields=['name', 'contents', 'name_en', 'contents_en'], 
                       fuzziness='auto')
        ).highlight_options(pre_tags='<span class="highlight">', post_tags='</span>')
        search_query = search_query.highlight('name', 'contents', 'name_en', 'contents_en')

        response = search_query[(int(page) - 1) * 10:int(page) * 10].execute()
        results = response.hits

        paginator = Paginator(results, 10)
        results = paginator.get_page(page)

    return render(request, 'search_app/search.html', {
        'query': query,
        'results': results
    })
