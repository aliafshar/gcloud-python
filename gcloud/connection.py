import httplib2


class Connection(object):
  """A generic connection to Google Cloud Platform.

  Subclasses should understand
  only the basic types
  in method arguments,
  however they should be capable
  of returning advanced types.
  """

  API_BASE_URL = 'https://www.googleapis.com'
  """The base of the API call URL."""

  _EMPTY = object()
  """A pointer to represent an empty value for default arguments."""

  def __init__(self, credentials=None):
    """
    :type credentials: :class:`gcloud.credentials.Credentials`
    :param credentials: The OAuth2 Credentials to use for this connection.
    """

    self._credentials = credentials

  @property
  def credentials(self):
    return self._credentials

  @property
  def http(self):
    """A getter for the HTTP transport used in talking to the API.

    :rtype: :class:`httplib2.Http`
    :returns: A Http object used to transport data.
    """
    if not hasattr(self, '_http'):
      self._http = httplib2.Http()
      if self._credentials:
        self._http = self._credentials.authorize(self._http)
    return self._http


class ApiClientConnection(Connection):
  """A generic connection that uses google-api-python-client."""

  API_NAME = None
  API_VERSION = None

  _service = None

  @property
  def service(self):
    """A getter for the api client service for making requests.

    This service is built once from discovery and cached. Unsetting
    :attr:`ApiClientConnection._service` will force a rebuild.

    :rtype: :class:`apiclient.discovery.Resource`
    :returns: an api client service
    """
    if not self._service:
      if not (self.API_NAME and self.API_VERSION):
        raise NotImplementedError(
            'API_NAME and API_VERSION must be set for ApiConnections.')
      from apiclient.discovery import build
      self._service = build(self.API_NAME, self.API_VERSION, http=self.http)
    return self._service


