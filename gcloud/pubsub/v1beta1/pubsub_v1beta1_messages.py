"""Generated message classes for pubsub version v1beta1.

Provides reliable, many-to-many, asynchronous messaging between applications.
"""

from protorpc import messages


package = 'pubsub'


class AcknowledgeRequest(messages.Message):
  """A AcknowledgeRequest object.

  Fields:
    ackId: The Ack ID for the message being acknowledged. This was returned by
      the Pub/Sub system in the Pull response.
    subscription: The subscription whose message is being acknowledged.
  """

  ackId = messages.StringField(1, repeated=True)
  subscription = messages.StringField(2)


class Label(messages.Message):
  """A key-value pair applied to a given object.

  Fields:
    key: The key of a label is a syntactically valid URL (as per RFC 1738)
      with the "scheme" and initial slashes omitted and with the additional
      restrictions noted below. Each key should be globally unique. The "host"
      portion is called the "namespace" and is not necessarily resolvable to a
      network endpoint. Instead, the namespace indicates what system or entity
      defines the semantics of the label. Namespaces do not restrict the set
      of objects to which a label may be associated.  Keys are defined by the
      following grammar:  key = hostname "/" kpath kpath = ksegment *[ "/"
      ksegment ] ksegment = alphadigit | *[ alphadigit | "-" | "_" | "." ]
      where "hostname" and "alphadigit" are defined as in RFC 1738.  Example
      key: spanner.google.com/universe
    numValue: A string attribute.
    strValue: A string attribute.
  """

  key = messages.StringField(1)
  numValue = messages.IntegerField(2)
  strValue = messages.StringField(3)


class ListSubscriptionsResponse(messages.Message):
  """A ListSubscriptionsResponse object.

  Fields:
    nextPageToken: If not empty, indicates that there are more subscriptions
      that match the request and this value should be passed to the next
      ListSubscriptionsRequest to continue.
    subscription: The subscriptions that match the request.
  """

  nextPageToken = messages.StringField(1)
  subscription = messages.MessageField('Subscription', 2, repeated=True)


class ListTopicsResponse(messages.Message):
  """A ListTopicsResponse object.

  Fields:
    nextPageToken: If not empty, indicates that there are more topics that
      match the request, and this value should be passed to the next
      ListTopicsRequest to continue.
    topic: The resulting topics.
  """

  nextPageToken = messages.StringField(1)
  topic = messages.MessageField('Topic', 2, repeated=True)


class ModifyAckDeadlineRequest(messages.Message):
  """A ModifyAckDeadlineRequest object.

  Fields:
    ackDeadlineSeconds: The new Ack deadline. Must be >= 1.
    ackId: The Ack ID.
    subscription: The name of the subscription from which messages are being
      pulled.
  """

  ackDeadlineSeconds = messages.IntegerField(1, variant=messages.Variant.INT32)
  ackId = messages.StringField(2)
  subscription = messages.StringField(3)


class ModifyPushConfigRequest(messages.Message):
  """A ModifyPushConfigRequest object.

  Fields:
    pushConfig: An empty push_config indicates that the Pub/Sub system should
      pause pushing messages from the given subscription.
    subscription: The name of the subscription.
  """

  pushConfig = messages.MessageField('PushConfig', 1)
  subscription = messages.StringField(2)


class PublishRequest(messages.Message):
  """A PublishRequest object.

  Fields:
    message: The message to publish.
    topic: The name of the topic for which the message is being added.
  """

  message = messages.MessageField('PubsubMessage', 1)
  topic = messages.StringField(2)


class PubsubEvent(messages.Message):
  """An event indicating a received message or truncation event.

  Fields:
    deleted: Indicates that this subscription has been deleted. (Note that
      pull subscribers will always receive NOT_FOUND in response in their pull
      request on the subscription, rather than seeing this boolean.)
    message: A received message.
    subscription: The subscription that received the event.
    truncated: Indicates that this subscription has been truncated.
  """

  deleted = messages.BooleanField(1)
  message = messages.MessageField('PubsubMessage', 2)
  subscription = messages.StringField(3)
  truncated = messages.BooleanField(4)


class PubsubMessage(messages.Message):
  """A message data and its labels.

  Fields:
    data: The message payload.
    label: Optional list of labels for this message. Keys in this collection
      must be unique.
  """

  data = messages.BytesField(1)
  label = messages.MessageField('Label', 2, repeated=True)


class PubsubSubscriptionsAcknowledgeResponse(messages.Message):
  """An empty PubsubSubscriptionsAcknowledge response."""


class PubsubSubscriptionsDeleteRequest(messages.Message):
  """A PubsubSubscriptionsDeleteRequest object.

  Fields:
    subscription: The subscription to delete.
  """

  subscription = messages.StringField(1, required=True)


class PubsubSubscriptionsDeleteResponse(messages.Message):
  """An empty PubsubSubscriptionsDelete response."""


class PubsubSubscriptionsGetRequest(messages.Message):
  """A PubsubSubscriptionsGetRequest object.

  Fields:
    subscription: The name of the subscription to get.
  """

  subscription = messages.StringField(1, required=True)


class PubsubSubscriptionsListRequest(messages.Message):
  """A PubsubSubscriptionsListRequest object.

  Fields:
    maxResults: Maximum number of subscriptions to return.
    pageToken: The value obtained in the last ListSubscriptionsResponse for
      continuation.
    query: A valid label query expression.
  """

  maxResults = messages.IntegerField(1, variant=messages.Variant.INT32)
  pageToken = messages.StringField(2)
  query = messages.StringField(3)


class PubsubSubscriptionsModifyAckDeadlineResponse(messages.Message):
  """An empty PubsubSubscriptionsModifyAckDeadline response."""


class PubsubSubscriptionsModifyPushConfigResponse(messages.Message):
  """An empty PubsubSubscriptionsModifyPushConfig response."""


class PubsubTopicsDeleteRequest(messages.Message):
  """A PubsubTopicsDeleteRequest object.

  Fields:
    topic: Name of the topic to delete.
  """

  topic = messages.StringField(1, required=True)


class PubsubTopicsDeleteResponse(messages.Message):
  """An empty PubsubTopicsDelete response."""


class PubsubTopicsGetRequest(messages.Message):
  """A PubsubTopicsGetRequest object.

  Fields:
    topic: The name of the topic to get.
  """

  topic = messages.StringField(1, required=True)


class PubsubTopicsListRequest(messages.Message):
  """A PubsubTopicsListRequest object.

  Fields:
    maxResults: Maximum number of topics to return.
    pageToken: The value obtained in the last ListTopicsResponse for
      continuation.
    query: A valid label query expression.
  """

  maxResults = messages.IntegerField(1, variant=messages.Variant.INT32)
  pageToken = messages.StringField(2)
  query = messages.StringField(3)


class PubsubTopicsPublishResponse(messages.Message):
  """An empty PubsubTopicsPublish response."""


class PullRequest(messages.Message):
  """A PullRequest object.

  Fields:
    returnImmediately: If this is specified as true the system will respond
      immediately even if it is not able to return a message in the Pull
      response. Otherwise the system is allowed to wait until at least one
      message is available rather than returning FAILED_PRECONDITION. The
      client may cancel the request if it does not wish to wait any longer for
      the response.
    subscription: The subscription from which a message should be pulled.
  """

  returnImmediately = messages.BooleanField(1)
  subscription = messages.StringField(2)


class PullResponse(messages.Message):
  """Either a PubsubMessage or a truncation event. One of these two must be
  populated.

  Fields:
    ackId: This ID must be used to acknowledge the received event or message.
    pubsubEvent: A pubsub message or truncation event.
  """

  ackId = messages.StringField(1)
  pubsubEvent = messages.MessageField('PubsubEvent', 2)


class PushConfig(messages.Message):
  """Configuration for a push delivery endpoint.

  Fields:
    pushEndpoint: A URL locating the endpoint to which messages should be
      pushed. For example, a Webhook endpoint might use
      "https://example.com/push".
  """

  pushEndpoint = messages.StringField(1)


class StandardQueryParameters(messages.Message):
  """Query parameters accepted by all methods.

  Enums:
    AltValueValuesEnum: Data format for the response.

  Fields:
    alt: Data format for the response.
    fields: Selector specifying which fields to include in a partial response.
    key: API key. Your API key identifies your project and provides you with
      API access, quota, and reports. Required unless you provide an OAuth 2.0
      token.
    oauth_token: OAuth 2.0 token for the current user.
    prettyPrint: Returns response with indentations and line breaks.
    quotaUser: Available to use for quota purposes for server-side
      applications. Can be any arbitrary string assigned to a user, but should
      not exceed 40 characters. Overrides userIp if both are provided.
    trace: A tracing token of the form "token:<tokenid>" to include in api
      requests.
    userIp: IP address of the site where the request originates. Use this if
      you want to enforce per-user limits.
  """

  class AltValueValuesEnum(messages.Enum):
    """Data format for the response.

    Values:
      json: Responses with Content-Type of application/json
    """
    json = 0

  alt = messages.EnumField('AltValueValuesEnum', 1, default=u'json')
  fields = messages.StringField(2)
  key = messages.StringField(3)
  oauth_token = messages.StringField(4)
  prettyPrint = messages.BooleanField(5, default=True)
  quotaUser = messages.StringField(6)
  trace = messages.StringField(7)
  userIp = messages.StringField(8)


class Subscription(messages.Message):
  """A subscription resource.

  Fields:
    ackDeadlineSeconds: For either push or pull delivery, the value is the
      maximum time after a subscriber receives a message before the subscriber
      should acknowledge or Nack the message. If the Ack deadline for a
      message passes without an Ack or a Nack, the Pub/Sub system will
      eventually redeliver the message. If a subscriber acknowledges after the
      deadline, the Pub/Sub system may accept the Ack, but it is possible that
      the message has been already delivered again. Multiple Acks to the
      message are allowed and will succeed.  For push delivery, this value is
      used to set the request timeout for the call to the push endpoint.  For
      pull delivery, this value is used as the initial value for the Ack
      deadline. It may be overridden for a specific pull request (message)
      with ModifyAckDeadline. While a message is outstanding (i.e. it has been
      delivered to a pull subscriber and the subscriber has not yet Acked or
      Nacked), the Pub/Sub system will not deliver that message to another
      pull subscriber (on a best-effort basis).
    name: Name of the subscription.
    pushConfig: If push delivery is used with this subscription, this field is
      used to configure it.
    topic: The name of the topic from which this subscription is receiving
      messages.
  """

  ackDeadlineSeconds = messages.IntegerField(1, variant=messages.Variant.INT32)
  name = messages.StringField(2)
  pushConfig = messages.MessageField('PushConfig', 3)
  topic = messages.StringField(4)


class Topic(messages.Message):
  """A topic resource.

  Fields:
    name: Name of the topic.
  """

  name = messages.StringField(1)


