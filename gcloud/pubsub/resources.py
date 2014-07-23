
import v1beta1.pubsub_v1beta1_messages as messages

from gcloud.pubsub import core
from gcloud.pubsub import utils


class FqrnNameProperty(object):

  def __init__(self, resource_type):
    self.resource_type = resource_type

  def __set__(self, obj, value):
    if utils.is_fully_qualified_name(self.resource_type, value):
      name = value
    else:
      if not obj.project:
        raise ValueError('project name must be set on the resource')
      name = utils.get_fully_qualified_name(
          obj.project, self.resource_type, value)
    obj.message.name = name

  def __get__(self, obj, value):
    return utils.get_unqualified_name(obj.message.name)


def requires_connection(f):
  """Requires that the resource has a known connection instance.

  :param f: Function/method to decorate.
  :returns: The decorated function.
  """
  def _check_connection(self, *args, **kw):
    if not (self.connection and self.project):
      raise ValueError()
    return f(*args, **kw)
  return _check_connection


class Resource(core.MessageProxy):

  project = None

  fully_qualified_name = core.MessageProperty('name')

  def __init__(self, message=None, connection=None, project=None):
    super(Resource, self).__init__(message)
    self.connection = connection
    self.project = project


class Topic(Resource):

  message_type = messages.Topic

  name = FqrnNameProperty('topics')

  @requires_connection
  def subscribe(self, subscription_name):
    return self.connection.subscribe(self, subscription_name)

  @requires_connection
  def delete(self):
    return self.connecton.delete_topic(self)

  @requires_connection
  def publish(self, message):
    return self.connection.publish(self, message)


class Subscription(Resource):

  message_type = messages.Subscription

  topic = core.MessageProperty('topic')
  ack_deadline = core.MessageProperty('ackDeadlineSeconds')

  def get_push_endpoint(self):
    return self.message.pushConfig.pushEndpoint

  def set_push_endpoint(self, uri):
    self.message.pushConfig.pushEndpoint = uri

  push_endpoint = property(get_push_endpoint, set_push_endpoint)

  @requires_connection
  def pull(self):
    return self.connection.pull(self)

  @requires_connection
  def items(self, timeout=60):
    for message in self.connection.iter_messages(self):
      yield message

  def __iter__(self):
    return self.items()


class Notification(core.MessageProxy):
  @requires_connection
  def ack(self):
    return self.connection.ack(self)



