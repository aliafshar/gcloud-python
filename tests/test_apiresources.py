
import unittest2

from gcloud.apiresources import ApiResource, ApiProperty, ApiListProperty


class Resource(ApiResource):

  name = ApiProperty('name', str)
  tags = ApiListProperty('tags')


class ResourceTest(unittest2.TestCase):

  def test_resource_property(self):
    r = Resource()
    r.name = 'banana'
    self.assertEqual({'name': 'banana'}, r.to_dict())

  def test_unset_value(self):
    r = Resource()
    self.assertEqual(None, r.name)

  def test_missing_attribute(self):
    r = Resource()
    self.assertRaises(AttributeError, lambda: r.missing)

  def test_resource_parent(self):
    r1 = Resource()
    r2 = Resource(parent=r1)
    self.assertIs(r1, r2.parent)

