"""The main shortcut methods for interacting with the Google Cloud DNS API."""

from gcloud.credentials import Credentials
from gcloud.dns.connection import Connection

#: Version of this package.
__version__ = '0.1'

#: Auth scope used for DNS.
DNS_SCOPE = 'https://www.googleapis.com/auth/ndev.clouddns.readwrite'


def get_connection(project, email, private_key_path, scopes=None):
  """Shortcut for establishing a connection with Cloud DNS.

  :type project: string
  :param project: The name of the project to connect to.

  :type client_email: string
  :param client_email: The e-mail attached to the service account.

  :type private_key_path: string
  :param private_key_path: The path to a private key file (this file was
                           given to you when you created the service
                           account).

  :rtype: :class:`gcloud.dns.connection.Connection`
  :returns: A connection defined with the proper credentials.
  """
  scopes = scopes or DNS_SCOPE
  credentials = Credentials.get_for_service_account(
      email, private_key_path, scopes)
  return Connection(credentials=credentials, project=project)


def get_zone(zone, project, email, private_key_path):
  """Shortcut for fetching a managed zone from Cloud DNS.

  If you already have a zone, this function will likely be your quickest entry
  point.

  :type zone: string
  :param zone: The name of the managed zone to fetch.

  :type project: string
  :param project: The name of the project to connect to.

  :type client_email: string
  :param client_email: The e-mail attached to the service account.

  :type private_key_path: string
  :param private_key_path: The path to a private key file (this file was
                           given to you when you created the service
                           account).

  :rtype: :class:`gcloud.dns.resources.Zone`
  :returns: A connection defined with the proper credentials.
  """
  connection = get_connection(project, email, private_key_path)
  return connection.get_zone(zone)

