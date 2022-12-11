import os
import re

from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from employees.utils import get_data_from_redis


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_structure(request):
    html_code: str = get_data_from_redis()
    template_file = os.path.join(os.getcwd(), 'employees', 'templates', 'index.html')

    with open(template_file, 'r', encoding='utf-8') as f:
        template_data = ''.join(f.readlines())

    template_data = re.sub("{{content}}", html_code, template_data)

    return HttpResponse(template_data)
