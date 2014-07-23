"""Connection for Google Cloud PubSub API.

With this connection instance you should be able to perform all the operations of this API.
"""

from apitools.base.py.exceptions import HttpError


# TODO(afshar): What happens when the API version changes.
from gcloud.pubsub.v1beta1.pubsub_v1beta1_client import PubsubV1beta1
import gcloud.pubsub.v1beta1.pubsub_v1beta1_messages as messages

from gcloud.pubsub import resources
from gcloud.pubsub import core
from gcloud.pubsub import utils


class Connection(object):
  """Connection for pubsub API."""

  _client_type = PubsubV1beta1

  def __init__(self, project, credentials=None):
    """
    :type credentials: :class:`gcloud.credentials.Credentials`
    :param credentials: The OAuth2 Credentials to use for this connection.
    """
    self._client = None
    self.credentials = credentials
    self.project = project

  @property
  def client(self):
    """Get or create the cached apitools client.

    :returns: The client.
    """
    if self._client is None:
      self._client = self.create_client(credentials=self.credentials)
    return self._client

  def create_topic(self, topic_or_name):
    """Creates a topic.

    :param topic_or_name: Topic name (simple or fully qualified) or topic instance
    :type topic: str or :class:`gcloud.pubsub.Topic`
    :returns: The newly created topic.
    :rtype: :class:`gcloud.pubsub.Topic`
    """
    request_topic = resources.Topic(project=self.project)
    request_topic.name = self.get_topic_name(topic_or_name)
    response = self.client.topics.Create(request_topic.message)
    return resources.Topic(message=response, project=self.project,
        connection=self)

  def delete_topic(self, topic_or_name):
    request = messages.PubsubTopicsDeleteRequest()
    request.topic = self.get_topic_name(topic_or_name)
    self.client.topics.Delete(request)

  def get_topic(self, topic_or_name):
    """get_topic

    :param topic_or_name:
    :type topic_or_name:
    :returns:
    :rtype:
    """
    request = messages.PubsubTopicsGetRequest()
    request.topic = self.get_topic_name(topic_or_name)
    response = self.client.topics.Get(request)
    return resources.Topic(response, connection=self, project=self.project)

  def list_topics(self):
    """list_topics

    :returns:
    :rtype:
    """
    request = messages.PubsubTopicsListRequest()
    request.query = utils.get_project_query(self.project)
    return (
        resources.Topic(msg, project=self.project, connection=self)
        for msg in core.ApitoolsIterator(
            self.client.topics.List, request, items_key='topic'))

  def subscribe(self, topic, name):
    """Subscribes to a topic.

    :param topic: The topic to subscribe to, either as a topic or a name.
    :type topic: :class:`gcloud.pubsub.topic.Topic` or str
    :param name: The name of the subscription.
    :type name: str
    :returns: The newly created subscription.
    :rtype: :class:`gcloud.pubsub.subscription.Subscription`.
    """
    request = messages.Subscription()
    request.topic = self.get_topic_fqrn()
    request.name = self.get_subscription_fqrn(name)
    response = self.client.subscriptions.Create(request)
    return response

  def pull(self, subscription, wait=False):
    """Pulls a notification message.

    Note: this will not wait indefinitely even with wait=True, because there is
    the possibility of HTTP client timeouts, etc.

    :param subscription: The subscription or subscription name to pull.
    :type subscription: str or :class:`gcloud.pubsub.subscription`
    """
    request = messages.PullRequest()
    if hasattr(subscription, 'name'):
      subscription_name = subscription.name
    else:
      subscription_name = self.get_subscription_fqrn(subscription)
    request.subscription = subscription_name
    request.returnImmediately = not wait
    # The API returns a 400 if there are no messages to pull, and we are in
    # immediate mode. This is an error, but likely not suitable for throwing as
    # an exception here because it is an entirely expected situation. We should
    # return None to indicate that there are no messages.
    try:
      response = self.client.subscriptions.Pull(request)
    except HttpError as e:
      # TODO(afshar): parse the error message and decide if it really is the
      # right error. (!)
      response = None
    return response

  def wait(self, subscription):
    """Wait for a notification, polling past timeouts, etc."""
    notification = None
    while not notification:
      notification = self.pull(subscription, wait=True)
    return notification

  def iter_messages(self, subscription):
    """iter_messages

    :param subscription:
    :type subscription:
    """
    while 1:
      yield self.wait(subscription)

  def publish(self, topic, message_bytes):
    """Publishes a message to a topic."""
    request = messages.PublishRequest()
    request.message = messages.PubsubMessage()
    request.message.data = message_bytes
    request.topic = self.get_topic_fqrn(topic)
    response = self.client.topics.Publish(request)
    return response

  def ack(self, subscription, *acks):
    """Acks one or more subscription requests.

    :param subscription:
    :type subscription:
    :param *acks: A sequence of ackable things, ids or notification.
    :type *acks: str or :class:`pubsub.Notification`
    """
    ack_ids = []
    for ack in acks:
      if hasattr(ack, 'ackId'):
        ack_id = ack.ackId
      else:
        ack_id = ack
      ack_ids.append(ack_id)
    request = messages.AcknowledgeRequest()
    request.subscription = self.get_subscription_name(subscription)
    request.ackId = ack_ids
    response = self.client.subscriptions.Acknowledge(request)
    return response

  def get_resource_name(self, resource_or_name, resource_type):
    return utils.get_resource_name(resource_or_name, resource_type, self.project)

  def get_topic_name(self, topic_name):
    return self.get_fully_qualified_name('topics', topic_name)

  def get_subscription_name(self, subscription_name):
    return self.get_fully_qualified_name('subscriptions', subscription_name)

