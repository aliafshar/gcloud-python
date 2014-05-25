

from gcloud.apiresrouces import ApiResource, ApiProperty


class Zone(ApiResource):
  """A Managed DNS Zone.

  This provides all the data and functionality required for zone management.
  Likely you will not instantiate this class directly, but use
  :py:func:`gcloud.dns.get_zone` or
  :py:func:`gcloud.dns.connection.Connection.get_zone`.
  """
  #: Name of the zone.
  #: REQUIRED for zone creation.
  name = ApiProperty('name', str)

  #: DNS Name of the zone. (api property `dns_name`)
  #: REQUIRED for zone creation.
  dns_name = ApiProperty('dnsName', str)

  #: Description of the zone. (api property `description`)
  #: REQUIRED for zone creation
  description = ApiProperty('description', str)

  @property
  def project(self):
    return self.parent

  def add_record(self, **kw):
    """Add a record to this zone.

    For a list of keyword arguments, please see
    :py:func:`cloud.dns.connection.Connection.add_record`.
    """
    return self.connection.add_record(self, **kw)

  def delete_record(self, **kw):
    return self.connection.delete_record(self, **kw)

  def create(self):
    pass

  def delete(self):
    zone = get_attr_or_string(zone, 'name')
    args = self._default_args(managedZone=zone, project=project_id)
    self.svc.managedZones().delete(
        managedZone=self.name,
        project=self.project.name).execute()
    return True

  def update(self):
    pass

  def validate_for_create(self):
    if not all([self.name, self.dns_name, self.description]):
      raise ValueError(
        'name, dns_name and description are required to create a zone.')


class Record(ApiResource):
  """A DNS Record.
  """

  _original_state = None

  name = ApiProperty('name', str)
  ttl = ApiProperty('ttl', int)
  type = ApiProperty('type', str)
  data = ApiProperty('rrdatas', list)

  def __init__(self, *args, **kw):
    super(Record, self).__init__(*args, **kw)
    self._original_state = self.raw.copy()
    if not self.data:
      self.data = []

  def get_original(self):
    return Record.from_dict(self.connection, self._original_state)

  def save(self):
    self.connection.update_record(self)

  @classmethod
  def from_dict(cls, data, parent=None, connection=None):
    resource = super(Record, cls).from_dict(data, parent, connection)
    resource._original_state = resource.to_dict().copy()
    return resource

  @classmethod
  def from_dnspython(cls, rdataset, name=None, parent=None, connection=None):
    from gcloud.dns.ext.dnspython import convert_record
    record = convert_record(rdataset, name)
    if parent:
      record.parent = parent
    if connection:
      record.connection = connection
    return record


class Change(ApiResource):
  """A change to a DNS zone.

  A change contains any number of record additions and deletions. Normally, you
  will not use this class, but instead call add_record, and delete_record from
  the zone or the connection.

  You can use this class for more complicated change creation.

  >>> c = Change(connection)
  >>> c.add(Record(type='A', ttl=60, name='test1.aliafshar.org.'))
  >>> c.delete(Record(type='A', ttl=60, name='test2.aliafshar.org.'))
  >>> connection.apply_change(c)
  """

  def _append_record(self, record, action):
    if not self.raw.get(action):
      self.raw[action] = []
    self.raw[action].append(record.as_dict())

  def add(self, record):
    return self._append_record(record, 'additions')

  def delete(self, record):
    return self._append_record(record, 'deletions')

  def update(self, record):
    self.delete(record.get_original())
    self.add(record)

    print record.get_original().as_dict()

