

class Pretty(object):
  def __repr__(i):
    return i.__class__.__name__ + kv(i.__dict__)

  def kv(d):
      return '(' + ', '.join(['%s: %s' % (k, d[k])
                              for k in sorted(d.keys())
                              if k[0] != "_"]) + ')'

class O(Pretty):
  def __init__(i, **adds): i.__dict__.update(adds)
