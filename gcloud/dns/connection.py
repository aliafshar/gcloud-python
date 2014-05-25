

from gcloud.apiresources import get_or_create_instance, get_attr_or_string
from gcloud.connection import ApiClientConnection

from gcloud.dns.iterators import MethodIterator
from gcloud.dns.resources import Zone, Record, Change



class Connection(ApiClientConnection):
  """Connection to Google Cloud DNS API."""

  API_NAME = 'dns'
  API_VERSION = 'v1beta1'

  def __init__(self, project=None, credentials=None):
    self.project = project
    super(Connection, self).__init__(credentials=credentials)

  def list_zones(self):
    """Iterates over the zones in this project."""
    return MethodIterator(
        connection=self,
        request_method=self.service.managedZones().list,
        request_args={'project': self.project},
        as_type=Zone,
        items_key='managedZones'
    )

  def create_zone(self, zone=None, name=None, dns_name=None, description=None):
    """Creates a managed zone.

    >>> c.create_zone(name='myzone', dns_name='example.com.')
    >>> <Zone:...>

    or if you already have a zone instance,

    >>> z = Zone(name='myzone', dns_name='example.com.')
    >>> c.create_zone(zone=z)
    """
    zone = get_or_create_instance(zone, Zone)
    if name:
      zone.name = name
    if dns_name:
      zone.dns_name = dns_name
    if description:
      zone.description = description
    #: Throws ValueError if zone is missing information
    zone.validate_for_create()
    response = self.service.managedZones().create(
        body=zone.to_dict(),
        project=self.project).execute()
    return Zone.from_dict(response, connection=self)

  def delete_zone(self, zone, project_id=None):
    """Deletes a manages zone.

    :param zone:
    :ptype zone:
    """
    zone = get_attr_or_string(zone, 'name')
    args = self._default_args(managedZone=zone, project=project_id)
    self.svc.managedZones().delete(**args).execute()

  def get_zone(self, zone, project_id=None):
    zone = get_attr_or_string(zone, 'name')
    args = self._default_args(managedZone=zone, project=project_id)
    response = self.svc.managedZones().get(**args).execute()
    return Zone.from_dict(self.connection, response)

  def list_records(self, zone, type=None, name=None, project=None):
    zone = get_attr_or_string(zone, 'name')
    return self._iterator_for(
        self.svc.resourceRecordSets().list,
        {'type': type, 'name': name, 'managedZone': zone},
        Record,
        items_key='rrsets',
    )

  def apply_change(self, zone, change, project_id=None):
    args = self._default_args(managedZone=zone, project=project_id)
    response = self.svc.changes().create(
        body=change.as_dict(), **args).execute()
    return self._construct(Change, response)

  def add_record(self, zone, name=None, type=None, ttl=None, data=None,
      record=None, project_id=None):
    zone = get_attr_or_string(zone, 'name')
    record = get_or_create_instance(record, Record)
    if name:
      record.name = name
    if type:
      record.type = type
    if ttl:
      record.ttl = ttl
    if data:
      record.data = data
    change = self._construct(Change)
    change.add(record)
    return self.apply_change(zone, change, project_id)

  def add_records(self, zone, records, project_id=None):
    zone = get_attr_or_string(zone, 'name')
    change = self._construct(Change)
    for record in records:
      change.add(record)
    return self.apply_change(zone, change, project_id)

  def delete_record(self, zone, record, project_id=None):
    zone = get_attr_or_string(zone, 'name')
    if not isinstance(record, Record):
      raise TypeError('record must be a Record')
    change = self._construct(Change)
    change.delete(record)
    return self.apply_change(zone, change, project_id)

  def update_record(self, zone, record, project_id=None):
    zone = get_attr_or_string(zone, 'name')
    if not isinstance(record, Record):
      raise TypeError('record must be a Record')
    change = self._construct(Change)
    change.update(record)
    return self.apply_change(zone, change, project_id)

  def _get_project_or_default_project(self, project):
    if isinstance(Project, project):
      return project
    elif project:
      return Project(connection=self, name=project)
    elif self.project:
      return Project(connection=self, name=self.project)
    raise ValueError('Connection must have a project, or project must be '
                     'passed explicitly.')

  def _default_args(self, **kw):
    args = {}
    args.update({'project': self.project})
    for k, v in kw.items():
      if v is not None:
        args[k] = v
    return args

  def _iterator_for(self, method, args, as_type, **kw):
    return MethodIterator(self, method, request_args=self._default_args(**args),
        as_type=as_type, **kw)
