"""Utilities used by pubsub."""


def get_fully_qualified_name(project, resource_type, resouce_name):
  """Create a fully qualified resource identifier.

  :param project: The project name.
  :type project: string
  :param resource_type: The type of resource ("topics" or "subscriptions").
  :type resource_type: string
  :param resouce_name: The name of the resource.
  :type resouce_name: string

  :returns: The generated resource identifier.
  :rtype: str
  """
  return '/{}/{}/{}'.format(resource_type, project, resouce_name)


def is_fully_qualified_name(resource_type, name):
  return name.startswith('/{}/'.format(resource_type))


def get_unqualified_name(name):
  return name.rsplit('/', 1)[-1]


def get_resource_name(resource_or_name, resource_type, project):
  if hasattr(resource_or_name, 'fully_qualified_name'):
    return resource_or_name.fully_qualified_name
  else:
    if is_fully_qualified_name(resource_type, resource_or_name):
      return resource_or_name
    else:
      return get_fully_qualified_name(project, resource_type, resource_or_name)


def get_project_query(project):
  """Create a query suitable for filtering resources by project.

  :param project: The project name.
  :type project: str

  :returns: The generated project query.
  :rtype: str
  """
  return 'cloud.googleapis.com/project in (/projects/{})'.format(project)
