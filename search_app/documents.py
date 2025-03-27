from django_elasticsearch_dsl import Document, Index, fields
from .models import StandardDoc

standard_index = Index('standard_docs')

@standard_index.doc_type
class StandardDocDocument(Document):
    class Django:
        model = StandardDoc
        fields = [
            'code_type',
            'code',
            'name',
            'contents'
        ]