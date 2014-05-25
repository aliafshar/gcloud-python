"""Iterators. An abstraction that pythonifies API list responses.

The problem:

Many API requests have the pattern that they return a paginated list of results.

These requests differ in 3 ways:
1. How the actual data is fetched
2. How the results are extracted from the result data
3. The type of the final results

These requests are identical in that:

1. Paginating must be handled
2. A Python generator is the best way to represent all results
3. Some constant arguments will be required for every requests
4. Different requests differ by a page token
"""

DEFAULT_ITEMS_KEY = 'items'


class Iterator(object):
  """A generic class for iterating through API list responses.

  :type connection: :class:`gcloud.storage.connection.Connection`
  :param connection: The connection to use to make requests.

  :type path: string
  :param path: The path to query for the list of items.
  """

  page_number = 0
  next_page_token = None

  def __init__(self, connection, request_args=None, as_type=None,
      items_key=None):
    self.connection = connection
    self.request_args = request_args or {}
    self.as_type = as_type
    self.items_key = items_key or DEFAULT_ITEMS_KEY

  def get_next_page_response(self):
    """Requests the next page from the path provided.

    :rtype: dict
    :returns: The parsed JSON response of the next page's contents.
    """
    raise NotImplementedError

  def get_items_from_response(self, response):
    """Factory method called while iterating. This should be overriden.

    This method can be overridden by a subclass. It should accept the API
    response of a request for the next page of items, and return a list (or
    other iterable) of items.

    The default implementation just grabs the value of 'items' from the
    response, which will suffice a large majority of cases.

    :type response: dict
    :param response: The response of asking for the next page of items.

    :rtype: iterable
    :returns: Items that the iterator should yield.
    """
    print response
    return response[self.items_key]

  def __iter__(self):
    """Iterate through the list of items."""
    while self.has_next_page():
      response = self.get_next_page_response()
      self.page_number += 1
      self.next_page_token = response.get('nextPageToken')
      for item in self.get_items_from_response(response):
        yield self.construct_item(item)

  def construct_item(self, item):
    if self.as_type:
      return self.as_type.from_dict(item, connection=self.connection)
    return item

  def has_next_page(self):
    """Determines whether or not this iterator has more pages.

    :rtype: bool
    :returns: Whether the iterator has more pages or not.
    """
    if self.page_number == 0:
      return True

    return self.next_page_token is not None

  def get_query_params(self):
    """Getter for query parameters for the next request.

    :rtype: dict or None
    :returns: A dictionary of query parameters or None if there are none.
    """
    params = self.request_args.copy()
    if self.next_page_token:
      params['pageToken'] = self.next_page_token
    return params

  def reset(self):
    """Resets the iterator to the beginning."""
    self.page_number = 0
    self.next_page_token = None


class MethodIterator(Iterator):

  def __init__(self, connection, request_method, request_args, as_type=None, items_key=None):
    super(MethodIterator, self).__init__(connection, request_args, as_type,
        items_key)
    self.request_method = request_method

  def get_next_page_response(self):
    return self.request_method(**self.get_query_params()).execute()
