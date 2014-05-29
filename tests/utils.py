

class DummyRequest(object):
  """Helper to represent an HTTP request."""

  def __init__(self, uri, method, body):
    self.uri = uri
    self.method = method
    self.body = body


class HttpRecorder(object):
  """Helper for stubbing out an httplib2 client.

  This class performs two roles:

  1. It responds to requests with a sequence of responses that have been predefined.
  2. It records all requests for asserting correct parameters, urls, bodies etc.

  >>> r = HttpRecorder([({'status': '200'}, 'Hello world')])
  >>> r.request('http://google.com')
  {'status': '200'}, 'Hello World'
  >>> assert r.requests[0]
  """

  #: List of responses that will be returned on sequentially calling the recorder.
  responses = None

  #: List of requests that have been recorded by the recorder.
  requests = None

  #: List index that contains the state of which request we are on.
  request_index = 0

  def __init__(self, responses=None):
    self.responses = responses or self.responses or []
    self.requests = []

  def request(self, uri, method='GET', body=None, redirections=1, connection_type=None):
    """This method stubs out httplib2.Http.request."""
    self.requests.append(DummyRequest(uri, method, body))
    try:
      response = self.responses[self.request_index]
    except IndexError:
      # If we don't have enough responses, we raise an AssertionError mostly for
      # test friendliness.
      raise AssertionError('Not enough responses set for this recorder.')
    self.request_index += 1
    return response

