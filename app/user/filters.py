from django.db.models import Q
from django_filters import rest_framework as filters
from .models import CustomUser

class UserFilters(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='contains', label='username')
    class Meta:
        model = CustomUser
        fields = ['username']

class UserFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    search = filters.CharFilter(method='search_by_value', label='search')

    class Meta:
        model = CustomUser
        fields = ['username']

    def search_by_value(self, queryset, name, value):
        filter_params = Q()
        q_list = self.request.query_params.get('search').split()
        for i in q_list:
            filter_params |=Q(username__contains=i)
        output = queryset.filter(filter_params)
        return output
