
"""Generic types for handling hierarchical RESTful resources.

The common problems with dealing with RESTful API services are:

  1. Inconsistent internal state in data objects
  2. Handling hierarchical relationships

The goal of this module is to eliminate both of these problems. Internal state
is handled by delegating data access and mutation to an internal dict that is
eventually used as a request body or received as a response body. Hierarchy is
handled by forcing every non-root resource to identify a parent.

Let's look at an example in the compute engine API.

Project [the root node]
  + Zone
    + Disk
    + Instance
    ...

All disk operations require a knowledge of the Zone and Project that is
appropriate for the disk, but rarely should a developer have to pass this data
explicitly on every operation, so from a high-level creating a disk might look
like:

  >>> Project('1234567').get_zone('us-central1-a').create_disk(size=20)
  <Disk:...>

whereas the actual RESTful API takes a single request to create a disk that
requires passing the project and the zone.

This module defines some interfaces that can be considered as contractual and
used freely:

  1. Resource().to_dict, to retreieve the raw data representation of a resource.
  2. Resource.from_dict(data, parent), a constructor to generate a resource from
  given data 3. Resource().parent, the parent resource, or None if this is the
  root resource.
"""


class ApiProperty(object):
  """Descriptor to allow setting and reading a value from an underlying dict.

  >>> class Test(Model):
  ...   name = ApiProperty('name', str)
  ...
  >>> t = Test()
  >>> t.name = 'banana'
  >>> print t.name
  banana
  >>> print t.raw
  {'name': 'banana'}
  """

  def __init__(self, name, as_type=None):
    self.name = name
    self.as_type = as_type

  def __get__(self, obj, type=None):
    # This nasty hack is here to allow sphinx to auto-generate documentation
    # without explicitly marking all properties as "novalue". Sphinx attemtps to
    # read the value of this property and fails.
    print [obj]
    if not obj:
      return ''
    # End nasty hack
    raw = obj.to_dict().get(self.name)
    if self.as_type and raw is not None:
      return self.as_type(raw)
    else:
      return raw

  def __set__(self, obj, value):
    if hasattr(value, 'as_dict'):
      value = value.as_dict()
    obj.to_dict()[self.name] = value


class ApiListProperty(object):
  """Descriptor to allow setting and reading simple lists from an underlying dict.

  Note: this descriptor is only suitable for lists of data that are embedded in
  responses rather than those that are linked as collections.
  """
  def __init__(self, name, as_type=None):
    self.name = name
    self.as_type = as_type

  def __get__(self, obj, type=None):
    return list(self._list_items(obj))

  def _list_items(self, obj):
    for item in obj.raw[self.name] or []:
      yield self.type(connection=obj.connection, data=item)

  def __set__(self, obj, value):
    items = obj.raw[self.name] = []
    for item in value:
      if hasattr(value, 'as_dict'):
        item = value.as_dict()
      items.append(item)


class ApiResource(object):
  """A hierarchical resource that proxies data from an underlying dict.

  The underlying raw data in this class is identical to the data that
  is expected and received from APIs. Registering API properties should
  be performed by the :class:`ApiProperty` and :class:`ApiListProperty`
  descriptors which are responsible for accessing and mutating data in
  resources.

  It is expected that individual APIs will create hybrid delegate types which
  contain the data, but add functionality that is specific to that class and
  requires a knowledge of the hierarchy. For example, the compute engine API's
  Instance operations all require knowledge of the Project that an instance
  belongs to.

  >>> class MyResource(Resource):
  ...   name = ApiProperty('name')
  ...
  >>> r = MyResource()
  >>> r.name = 'banana'
  >>> r.as_dict()
  {'name': 'banana'}
  >>> MyResource.from_dict({'name': 'banana'}).name
  'banana'
  """

  #: The connection context of this resource. May be None.  It is recommended to
  #: call :func:`ApiResource.get_connection` instead which will look up the
  #: closest connection in the parent heirarchy.
  _connection = None

  #: The raw dict representation of this resource from which proprties are
  #: accessed and set.
  _raw = None

  #: The parent resource. May be None for unparented resources or root
  #: resrouces.
  _parent = None

  def __init__(self, parent=None, connection=None, **kw):
    self._raw = {}
    self._raw.update(kw)
    self._connection = connection
    self._parent = parent

  def __str__(self):
    return '<{}:{}>'.format(self.__class__.__name__, self.name)

  def get_connection(self):
    if self._connection:
      return self._connection
    elif self._parent:
      return self._parent.get_connection()
    else:
      return None

  def set_connection(self, value):
    self._connection = value

  connection = property(get_connection, set_connection)

  @classmethod
  def from_dict(cls, data, parent=None, connection=None):
    resource = cls(parent=parent, connection=connection)
    resource._raw.update(data)
    return resource

  def to_dict(self):
    return self._raw

  def get_parent(self):
    return self._parent

  def set_parent(self, parent):
    self._parent = parent

  parent = property(get_parent, set_parent)


def get_or_create_instance(value, as_type):
  """Helper to use an instance if it is available or create it if it is None.

  This is extremely useful in handling non-required function arguments where an
  instance may be passed, or a single critical value may be passed in which case
  an instance is created and the attribute set on that instance.
  """
  if value is None:
    return as_type()
  elif isinstance(value, as_type):
    return value
  else:
    raise ValueError('{} must be a {}, or None'.format(value, type))


def get_attr_or_string(value, attr):
  """Get an attribute from an instance, a dict, or return the given value.

  This is extremely useful when a value can be passed as an instance with a
  `name` attribute, or the name itself.
  """
  if hasattr(value, attr):
    return getattr(value, attr)
  elif hasattr(value, 'get'):
    return value.get(attr)
  else:
    return value

