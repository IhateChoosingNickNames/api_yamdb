from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    """Кастомная фильтрация поиска по Title."""

    def get_search_fields(self, view, request):
        params = []
        if request.query_params.get("category"):
            CustomSearchFilter.search_param = "category"
            params.append("category__slug")
        if request.query_params.get("genre"):
            CustomSearchFilter.search_param = "genre"
            params.append("genre__slug")
        if request.query_params.get("year"):
            CustomSearchFilter.search_param = "year"
            params.append("year")
        if request.query_params.get("name"):
            CustomSearchFilter.search_param = "name"
            params.append("name")

        if params:
            return params

        return super().get_search_fields(view, request)
