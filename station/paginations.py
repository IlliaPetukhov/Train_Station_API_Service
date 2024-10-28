from rest_framework.pagination import PageNumberPagination


class PaginationForShortSerializerData(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class PaginationForLongSerializerData(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class PaginationForTooLongSerializerData(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 10
