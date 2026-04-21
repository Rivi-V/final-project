from django.core.paginator import Paginator

from team_finder.constants import PROJECTS_PER_PAGE


def paginate_queryset(queryset, page_number, per_page=PROJECTS_PER_PAGE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)
