
# ref: https://morioh.com/p/cbde394bafac 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
class ViewPaginatorMixin(object):

    def paginate(self, object_list, type, page=1, size=10, **kwargs):
      min_size = 1
      max_size = 100
      try:
          page = int(page)
          if page < 1:
              page = 1
      except (TypeError, ValueError):
          page = 1

      try:
          size = int(size)
          if size < min_size:
              size = min_size
          if size > max_size:
              size = max_size
      except (ValueError, TypeError):
          size = max_size

      paginator = Paginator(object_list, size)
      try:
          objects = paginator.page(page)
      except PageNotAnInteger:
          objects = paginator.page(1)
      except EmptyPage:
          objects = paginator.page(paginator.num_pages)
      data = {
          'type': type,
          'items': list(objects)
      }
      return data