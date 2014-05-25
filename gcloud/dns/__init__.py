"""The main shortcut methods for interacting with the Google Cloud DNS API."""

from gcloud.credentials import Credentials
from gcloud.dns.connection import Connection

#: Auth scope used for DNS
DNS_SCOPE = 'https://www.googleapis.com/auth/ndev.clouddns.readwrite'


def get_connection(project, email, private_key_path, scopes=None):
  credentials = Credentials.get_for_service_account(
      email, private_key_path, DNS_SCOPE)
  return Connection(credentials=credentials, project=project)

def get_zone(name, project_id, email, private_key_path):
  c = get_connection(email, private_key_path, project_id)
  return c.get_zone(name)


