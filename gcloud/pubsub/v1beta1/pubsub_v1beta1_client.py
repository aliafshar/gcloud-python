"""Generated client library for pubsub version v1beta1."""
from apitools.base.py import base_api
import pubsub_v1beta1_messages as messages


class PubsubV1beta1(base_api.BaseApiClient):
  """Generated client library for service pubsub version v1beta1."""

  MESSAGES_MODULE = messages

  _PACKAGE = u'pubsub'
  _SCOPES = [u'https://www.googleapis.com/auth/pubsub']
  _VERSION = u'v1beta1'
  _CLIENT_ID = 'myclient'
  _CLIENT_SECRET = 'mysecret'
  _USER_AGENT = ''
  _CLIENT_CLASS_NAME = u'PubsubV1beta1'
  _URL_VERSION = u'v1beta1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None):
    """Create a new pubsub handle."""
    url = url or u'https://www.googleapis.com/pubsub/v1beta1/'
    super(PubsubV1beta1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params)
    self.subscriptions = self.SubscriptionsService(self)
    self.topics = self.TopicsService(self)

  class SubscriptionsService(base_api.BaseApiService):
    """Service class for the subscriptions resource."""

    def __init__(self, client):
      super(PubsubV1beta1.SubscriptionsService, self).__init__(client)
      self.__configs = {
          'Acknowledge': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'pubsub.subscriptions.acknowledge',
              ordered_params=[],
              path_params=[],
              query_params=[],
              relative_path=u'subscriptions/acknowledge',
              request_field='<request>',
              request_type_name=u'AcknowledgeRequest',
              response_type_name=u'PubsubSubscriptionsAcknowledgeResponse',
              supports_download=False,
          ),
          'Create': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'pubsub.subscriptions.create',
              ordered_params=[],
              path_params=[],
              query_params=[],
              relative_path=u'subscriptions',
              request_field='<request>',
              request_type_name=u'Subscription',
              response_type_name=u'Subscription',
              supports_download=False,
          ),
          'Delete': base_api.ApiMethodInfo(
              http_method=u'DELETE',
              method_id=u'pubsub.subscriptions.delete',
              ordered_params=[u'subscription'],
              path_params=[u'subscription'],
              query_params=[],
              relative_path=u'subscriptions/{+subscription}',
              request_field='',
              request_type_name=u'PubsubSubscriptionsDeleteRequest',
              response_type_name=u'PubsubSubscriptionsDeleteResponse',
              supports_download=False,
          ),
          'Get': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'pubsub.subscriptions.get',
              ordered_params=[u'subscription'],
              path_params=[u'subscription'],
              query_params=[],
              relative_path=u'subscriptions/{+subscription}',
              request_field='',
              request_type_name=u'PubsubSubscriptionsGetRequest',
              response_type_name=u'Subscription',
              supports_download=False,
          ),
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'pubsub.subscriptions.list',
              ordered_params=[],
              path_params=[],
              query_params=[u'maxResults', u'pageToken', u'query'],
              relative_path=u'subscriptions',
              request_field='',
              request_type_name=u'PubsubSubscriptionsListRequest',
              response_type_name=u'ListSubscriptionsResponse',
              supports_download=False,
          ),
          'ModifyAckDeadline': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'pubsub.subscriptions.modifyAckDeadline',
              ordered_params=[],
              path_params=[],
              query_params=[],
              relative_path=u'subscriptions/modifyAckDeadline',
              request_field='<request>',
              request_type_name=u'ModifyAckDeadlineRequest',
              response_type_name=u'PubsubSubscriptionsModifyAckDeadlineResponse',
              supports_download=False,
          ),
          'ModifyPushConfig': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'pubsub.subscriptions.modifyPushConfig',
              ordered_params=[],
              path_params=[],
              query_params=[],
              relative_path=u'subscriptions/modifyPushConfig',
              request_field='<request>',
              request_type_name=u'ModifyPushConfigRequest',
              response_type_name=u'PubsubSubscriptionsModifyPushConfigResponse',
              supports_download=False,
          ),
          'Pull': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'pubsub.subscriptions.pull',
              ordered_params=[],
              path_params=[],
              query_params=[],
              relative_path=u'subscriptions/pull',
              request_field='<request>',
              request_type_name=u'PullRequest',
              response_type_name=u'PullResponse',
              supports_download=False,
          ),
          }

      self.__upload_configs = {
          }

    def GetMethodConfig(self, method):
      return self.__configs.get(method)

    def GetMethodUploadConfig(self, method):
      return self.__upload_configs.get(method)

    def Acknowledge(self, request, global_params=None):
      """Acknowledges a particular received message: the Pub/Sub system can remove the given message from the subscription. Acknowledging a message whose Ack deadline has expired may succeed, but the message could have been already redelivered. Acknowledging a message more than once will not result in an error. This is only used for messages received via pull.

      Args:
        request: (AcknowledgeRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PubsubSubscriptionsAcknowledgeResponse) The response message.
      """
      config = self.GetMethodConfig('Acknowledge')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Create(self, request, global_params=None):
      """Creates a subscription on a given topic for a given subscriber. If the subscription already exists, returns ALREADY_EXISTS. If the corresponding topic doesn't exist, returns NOT_FOUND.

      Args:
        request: (Subscription) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Subscription) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Delete(self, request, global_params=None):
      """Deletes an existing subscription. All pending messages in the subscription are immediately dropped. Calls to Pull after deletion will return NOT_FOUND.

      Args:
        request: (PubsubSubscriptionsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PubsubSubscriptionsDeleteResponse) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Get(self, request, global_params=None):
      """Gets the configuration details of a subscription.

      Args:
        request: (PubsubSubscriptionsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Subscription) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    def List(self, request, global_params=None):
      """Lists matching subscriptions.

      Args:
        request: (PubsubSubscriptionsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListSubscriptionsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    def ModifyAckDeadline(self, request, global_params=None):
      """Modifies the Ack deadline for a message received from a pull request.

      Args:
        request: (ModifyAckDeadlineRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PubsubSubscriptionsModifyAckDeadlineResponse) The response message.
      """
      config = self.GetMethodConfig('ModifyAckDeadline')
      return self._RunMethod(
          config, request, global_params=global_params)

    def ModifyPushConfig(self, request, global_params=None):
      """Modifies the PushConfig for a specified subscription. This method can be used to suspend the flow of messages to an end point by clearing the PushConfig field in the request. Messages will be accumulated for delivery even if no push configuration is defined or while the configuration is modified.

      Args:
        request: (ModifyPushConfigRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PubsubSubscriptionsModifyPushConfigResponse) The response message.
      """
      config = self.GetMethodConfig('ModifyPushConfig')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Pull(self, request, global_params=None):
      """Pulls a single message from the server. If return_immediately is true, and no messages are available in the subscription, this method returns FAILED_PRECONDITION. The system is free to return an UNAVAILABLE error if no messages are available in a reasonable amount of time (to reduce system load).

      Args:
        request: (PullRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PullResponse) The response message.
      """
      config = self.GetMethodConfig('Pull')
      return self._RunMethod(
          config, request, global_params=global_params)

  class TopicsService(base_api.BaseApiService):
    """Service class for the topics resource."""

    def __init__(self, client):
      super(PubsubV1beta1.TopicsService, self).__init__(client)
      self.__configs = {
          'Create': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'pubsub.topics.create',
              ordered_params=[],
              path_params=[],
              query_params=[],
              relative_path=u'topics',
              request_field='<request>',
              request_type_name=u'Topic',
              response_type_name=u'Topic',
              supports_download=False,
          ),
          'Delete': base_api.ApiMethodInfo(
              http_method=u'DELETE',
              method_id=u'pubsub.topics.delete',
              ordered_params=[u'topic'],
              path_params=[u'topic'],
              query_params=[],
              relative_path=u'topics/{+topic}',
              request_field='',
              request_type_name=u'PubsubTopicsDeleteRequest',
              response_type_name=u'PubsubTopicsDeleteResponse',
              supports_download=False,
          ),
          'Get': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'pubsub.topics.get',
              ordered_params=[u'topic'],
              path_params=[u'topic'],
              query_params=[],
              relative_path=u'topics/{+topic}',
              request_field='',
              request_type_name=u'PubsubTopicsGetRequest',
              response_type_name=u'Topic',
              supports_download=False,
          ),
          'List': base_api.ApiMethodInfo(
              http_method=u'GET',
              method_id=u'pubsub.topics.list',
              ordered_params=[],
              path_params=[],
              query_params=[u'maxResults', u'pageToken', u'query'],
              relative_path=u'topics',
              request_field='',
              request_type_name=u'PubsubTopicsListRequest',
              response_type_name=u'ListTopicsResponse',
              supports_download=False,
          ),
          'Publish': base_api.ApiMethodInfo(
              http_method=u'POST',
              method_id=u'pubsub.topics.publish',
              ordered_params=[],
              path_params=[],
              query_params=[],
              relative_path=u'topics/publish',
              request_field='<request>',
              request_type_name=u'PublishRequest',
              response_type_name=u'PubsubTopicsPublishResponse',
              supports_download=False,
          ),
          }

      self.__upload_configs = {
          }

    def GetMethodConfig(self, method):
      return self.__configs.get(method)

    def GetMethodUploadConfig(self, method):
      return self.__upload_configs.get(method)

    def Create(self, request, global_params=None):
      """Creates the given topic with the given name.

      Args:
        request: (Topic) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Topic) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Delete(self, request, global_params=None):
      """Deletes the topic with the given name. All subscriptions to this topic are also deleted. Returns NOT_FOUND if the topic does not exist. After a topic is deleted, a new topic may be created with the same name.

      Args:
        request: (PubsubTopicsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PubsubTopicsDeleteResponse) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Get(self, request, global_params=None):
      """Gets the configuration of a topic. Since the topic only has the name attribute, this method is only useful to check the existence of a topic. If other attributes are added in the future, they will be returned here.

      Args:
        request: (PubsubTopicsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Topic) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    def List(self, request, global_params=None):
      """Lists matching topics.

      Args:
        request: (PubsubTopicsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListTopicsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    def Publish(self, request, global_params=None):
      """Adds a message to the topic. Returns NOT_FOUND if the topic does not exist.

      Args:
        request: (PublishRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (PubsubTopicsPublishResponse) The response message.
      """
      config = self.GetMethodConfig('Publish')
      return self._RunMethod(
          config, request, global_params=global_params)
