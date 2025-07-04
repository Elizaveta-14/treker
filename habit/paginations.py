from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    """Пагинация для модели HABIT"""

    page_size = 5
    page_query_param = "page_size"
    max_page_size = 15
