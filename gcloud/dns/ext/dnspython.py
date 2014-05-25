

import dns





def parse_zone_file(filename):
  pass



def parseZone():
  jsonOutput = {}
  additions = []

  zone_file = '%s.zone' % domain

  try:
    zone = dns.zone.from_file(zone_file, domain)

    for name, node in zone.nodes.items():
      rdatasets = node.rdatasets

      for rdataset in rdatasets:

        api_name = qualifyName(name)

        if rdataset.rdtype in SUPPORTED_RECORD_TYPES:
          addition = {
                      'name' : api_name,
                      'ttl' : str(rdataset.ttl),
                      'type' : rdatatype.to_text(rdataset.rdtype),
                      'kind' : 'dns#resourceRecordSet'
                      }
        elif rdataset.rdtype in [SOA,NS]:
          # Skip the SOA and NS records in this example. The
          # SOA record is generated as part of the managed zone
          # the NS records here aren't applicable because this
          # zone is using Google Cloud DNS rather than providing
          # its own name servers
          # In your situation, you might want to keep the NS
          # records, if so add them to the SUPPORTED_RECORD_TYPES
          continue

        # Array of records for this name/type combination
        rrdatas = []

        for rdata in rdataset:
          if rdataset.rdtype == MX:
            rrdatas.append('%s %s' % (rdata.preference, qualifyName(rdata.exchange)))
          if rdataset.rdtype == CNAME:
            rrdatas.append(qualifyName(rdata.target))
          if rdataset.rdtype == A:
            rrdatas.append(rdata.address)

        addition.update({'rrdatas' : rrdatas})
        additions.append(addition)

    jsonOutput.update({'additions' : additions })
    return jsonOutput

  except DNSException, e:
    if e.__class__ is NoSOA:
      print ('Check that your SOA line starts with a qualified domain and is in the form of: \n')
      print ('  example.com. IN      SOA     ns1.example.com. hostmaster.example.com. (')
    print e.__class__, e


def convert_record(name, rdataset):
  from gcloud.dns.record import Record
  record = Record(name=name,
                  ttl=str(rdataset.ttl),
                  type=dns.rdatatype.to_text(rdataset.rdtype))
  rrdatas = record.data
  for rdata in rdataset:
    if rdataset.rdtype == MX:
      rrdatas.append('%s %s' % (rdata.preference, qualifyName(rdata.exchange)))
    if rdataset.rdtype == CNAME:
      rrdatas.append(qualifyName(rdata.target))
    if rdataset.rdtype == A:
      rrdatas.append(rdata.address)
  return record


def convert_zone():


def qualify_name():
  dns_name = str(dns_name)
  if domain not in dns_name and dns_name != '@':
    return dns_name + '.' + domain + '.'
  else:
    # Catches the @ symbol case too.
    return domain + '.'
