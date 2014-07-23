"""Google Cloud Pubsub API.

Get started quickly with the API.

>>> from gcloud.pubsub import get_connection
>>> pubsub = get_connection('project-name-here',
...                         'long-email@googleapis.com',
...                         '/path/to/private.key')
>>> # then do other things
>>> pubsub.create_topic('my-topic')
>>> pubsub.subscribe('my-topic')

The main concepts with this API are:

:class:`gcloud.pubsub.connection.Connection`
"""


AUTH_SCOPE = 'https://www.googleapis.com/auth/pubsub'


def get_connection(project, client_email=None, private_key_path=None):
  """Gets a 

  :param project:
  :type project:
  :param client_email:
  :type client_email:
  :param private_key_path:
  :type private_key_path:
  :returns:
  :rtype:
  """
  from gcloud.pubsub.connection import Connection
  from gcloud.credentials import Credentials
  credentials = Credentials.get_for_service_account(
      client_email, private_key_path, AUTH_SCOPE)
  return Connection(project, credentials=credentials)
