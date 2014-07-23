
# TODO (afshar) move to gcloud-python-core



class NotImplementedAttribute(object):
  """Descriptor that requires subclasses implement their property."""

  def __init__(self, name):
    self.name = name

  def __get__(self, obj, type=None):
    e = NotImplementedError(
        'Attribute "{}" must be implemented.'.format(self.name))
    if not obj:
      # When sphinx autodoc is running.
      return e
    raise e


class MessageProperty(object):
  """A property that proxies a named message attribute."""

  def __init__(self, name):
    self.name = name

  def __get__(self, obj, type=None):
    if not obj:
      return None
    return getattr(obj.message, self.name)

  def __set__(self, obj, value):
    return setattr(obj.message, self.name, value)


class MessageProxy(object):
  """Proxy over protorpc messages."""

  message_type = NotImplementedAttribute('message_type')
  message = None

  def __init__(self, message=None):
    self.message = message or self.message_type()


class ApitoolsIterator(object):
  """Iterates over paginated requests.

  >>> request = messages.PubsubTopicsListRequest()
  >>> i = ApitoolsIterator(client.topics.List, request, items_key='topic')
  >>> for topic in i:
  ...   print topic
  ...
  <Topic:>
  <Topic:>

  :param method: API method to be called.
  :type method: how knows
  :param request: Request for the method. This is modified in place.
  :param items_key: The key for items in the response.
  :param page_token_key: The key for the page token in the response.
  :param next_page_token_key: The key for the next page token in the request.
  """

  #: The request to call for each page of requests.
  request = None

  #: The method to call for each page of requests.
  method = None

  #: The key for items in the response.
  items_key = 'items'

  #: The key for the page token in the response.
  page_token_key = 'pageToken'

  #: The key for the next page token in the request.
  next_page_token_key = 'nextPageToken'

  def __init__(self, method, request, items_key=None, page_token_key=None,
      next_page_token_key=None):
    self.request = request
    self.method = method
    self.items_key = items_key or self.items_key
    self.page_token_key = page_token_key or self.page_token_key
    self.next_page_token_key = next_page_token_key or self.next_page_token_key
    self.has_more_items = True

  def fetch_items(self):
    """Fetch the items by calling the request.

    :returns: The response from the method call.
    """
    return self.method(self.request)

  def extract_items(self, response):
    """Extract the list of items from the response."""
    return getattr(response, self.items_key)

  def __iter__(self):
    """Iterate every item in every page of results."""
    while self.has_more_items:
      response = self.fetch_items()
      next_page_token = getattr(response, self.next_page_token_key)
      for item in self.extract_items(response):
        yield item
      setattr(self.request, self.page_token_key, next_page_token)
      self.has_more_items = next_page_token is not None

