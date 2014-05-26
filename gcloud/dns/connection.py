from functools import partial

from gcloud.apiresources import get_or_create_instance, get_attr_or_string
from gcloud.connection import ApiClientConnection

from gcloud.dns.iterators import MethodIterator
from gcloud.dns.resources import Zone, Record, Change



class Connection(ApiClientConnection):
  """Connection to Google Cloud DNS API via the JSON REST API.

  Note:

  * The connection can perform all the tasks of the API. The rest of the library
  contains shortcut methods that call methods on the connection.

  * A connection is bound to a single project, so this should be passed in on
  instantiation
  """

  API_NAME = 'dns'
  API_VERSION = 'v1beta1'

  def __init__(self, project=None, credentials=None):
    self.project = project
    super(Connection, self).__init__(credentials=credentials)

  def list_zones(self):
    """Iterates over the zones in this project.

    >>> for zone in connection.list_zones():
    ...   print zone
    ...
    <Zone:...>
    <Zone:...>

    :rtype: Iterable of :class:`gcloud.dns.resources.Zone`
    :returns: The zones in this project.
    """
    return self._get_iterator(
        self.service.managedZones().list,
        self._get_args(),
        Zone,
        items_key='managedZones'
    )

  def create_zone_instance(self, zone):
    """Creates a managed zone from a zone instance.

    >>> z = Zone(name='myzone', dns_name='example.com.', 'My example zone.')
    >>> c.create_zone_instance(z)

    :type zone: :class:`gcloud.dns.resources.Zone`
    :param zone: The zone to create.

    :rtype: :class:`gcloud.dns.resource.Zone`
    :returns: The newly created zone. Note: this will not be the same instance
              as passed.
    """
    #: Throws ValueError if zone is missing information
    zone.validate_for_create()
    response = self.service.managedZones().create(
        body=zone.to_dict(),
        project=self.project).execute()
    return Zone.from_dict(response, connection=self)

  def create_zone(self, name, dns_name, description):
    """Creates a managed zone.

    >>> c.create_zone('myzone', 'example.com.', 'My example zone.')
    >>> <Zone:...>

    If you already have a zone instance, use
    :meth:`gcloud.dns.resources.Zone.create`.

    :type dns_name: string
    :param dns_name: The compete DNS name of the zone, e.g. `aliafshar.org.`

    :type description: string
    :param description: A freeform description of the zone.

    :rtype: class:`gcloud.dns.resource.Zone`
    :returns: The newly created Zone.
    """
    zone = Zone(connection=self, name=name, dns_name=dns_name,
        description=description)
    return self.create_zone_instance(zone)

  def delete_zone(self, zone):
    """Deletes a manages zone.

    :type zone: :class:`gcloud.dns.resources.Zone` or string
    :param zone: The zone or the name of the zone to delete.
    """
    zone = get_attr_or_string(zone, 'name')
    self.svc.managedZones().delete(
        project=self.project, managedZone=zone).execute()

  def get_zone(self, zone, project_id=None):
    """Fetches a manages zone.

    :type zone: :class:`gcloud.dns.resource.Zone` or string
    :param zone: The zone or the name of the zone to fetch.

    :rtype: class:`gcloud.dns.resource.Zone`
    :returns: The fetched Zone.
    """
    zone = get_attr_or_string(zone, 'name')
    response = self.svc.managedZones().get(
        **self._get_args(managedZone=zone)).execute()
    return Zone.from_dict(self.connection, response)

  def list_records(self, zone, type=None, name=None):
    """Lists all the records in a zone.

    >>> for record in connection.list_records('my-zone'):
    ...   print record
    ...
    <Record:...>
    <Record:...>

    :type zone: :class:`gcloud.dns.resources.Zone` or string
    :param zone: The zone or the name of the zone to fetch.

    :type type: string
    :param type: the type of record to return

    :type name: string
    :param name:

    :rtype: Iterable of :class:`gcloud.dns.resources.Record`
    :returns: The records in this zone.
    """
    zone = get_attr_or_string(zone, 'name')
    return self._iterator_for(
        self.svc.resourceRecordSets().list,
        self._get_args(type=type, name=name, managedZone = zone),
        partial(Record, parent=Zone(connection=self, name=zone)),
        items_key='rrsets',
    )

  def apply_change(self, zone, change):
    """Applies a change to a zone.

    Normally you do not need to manually apply a change. You can use the
    shortcuts :meth:`gcloud.dns.Connection.add_record`,
    :meth:`gcloud.dns.Connection.add_records`,
    :meth:`gcloud.dns.Connection.delete_record`,
    :meth:`gcloud.dns.Connection.update_record`.

    :type zone: :class:`gcloud.dns.Zone` or string
    :param zone: The zone or the name of the zone to fetch.

    :type change: :class:`gcloud.dns.Change`
    :param change: The change to apply.
    """
    zone = get_attr_or_string(zone, 'name')
    response = self.svc.changes().create(body=change.as_dict(),
        project=self.project, managedZone=zone).execute()
    return Change.fromDict(response, connection=self)

  def add_record(self, zone, name, type, ttl, data=None):
    """Adds a record to the given zone.

    >>> connection.add_record('my-zone', 'aliafshar.org.', 'A', 60, '1.2.3.4')
    <Change:...>

    :type zone: :class:`gcloud.dns.Zone` or string
    :param zone: The zone or the name of the zone to fetch.
    :type name: string
    :param name: The name of the record to add.
    :type name: string
    :param name: The name of the record to add.
    :rtype: :class:`gcloud.dns.Change`
    :returns: The change for the additon.
    """
    zone = get_attr_or_string(zone, 'name')
    record = Record(name=name, type=type, ttl=ttl)
    if data:
      record.data = data
    change = Change()
    change.add(record)
    return self.apply_change(zone, change)

  def add_records(self, zone, records):
    """Adds a number of records to a zone.

    :type zone: :class:`gcloud.dns.Zone` or string
    :param zone: The zone or the name of the zone to fetch.
    :type records: Iterable of :class:`gcloud.dns.Record`
    :param records: The records to add to this zone.
    """
    zone = get_attr_or_string(zone, 'name')
    change = self._construct(Change)
    for record in records:
      change.add(record)
    return self.apply_change(zone, change)

  def delete_record(self, zone, record):
    zone = get_attr_or_string(zone, 'name')
    if not isinstance(record, Record):
      raise TypeError('record must be a Record')
    change = self._construct(Change)
    change.delete(record)
    return self.apply_change(zone, change)

  def update_record(self, zone, record):
    zone = get_attr_or_string(zone, 'name')
    if not isinstance(record, Record):
      raise TypeError('record must be a Record')
    change = self._construct(Change)
    change.update(record)
    return self.apply_change(zone, change)

  def _get_args(self, **kw):
    args = {}
    args.update({'project': self.project})
    for k, v in kw.items():
      if v is not None:
        args[k] = v
    return args

  def _get_iterator(self, method, args, as_type, parent=None, **kwargs):
    """Utility method to ease creating iterators bound to this connection."""
    if parent:
      as_type = partial(as_type, parent=parent)
    return MethodIterator(
        connection=self,
        request_method=method,
        request_args=args,
        as_type=as_type,
        **kwargs)

