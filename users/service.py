from django.core.paginator import Paginator

from team_finder.constants import USERS_PER_PAGE


def paginate_queryset(queryset, page_number, per_page=USERS_PER_PAGE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def apply_variant_one_filter(queryset, current_user, active_filter):
    if active_filter == 'owners-of-favorite-projects':
        return queryset.filter(owned_projects__interested_users=current_user)
    if active_filter == 'owners-of-participating-projects':
        return queryset.filter(owned_projects__participants=current_user)
    if active_filter == 'interested-in-my-projects':
        return queryset.filter(favorites__owner=current_user)
    if active_filter == 'participants-of-my-projects':
        return queryset.filter(participated_projects__owner=current_user)
    return queryset
