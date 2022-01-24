class LocalCache:
  def __init__(self, query, valueEventHandler=None, childAddedHandler=None, childRemovedHandler=None, childChangedHandler=None):
    self.listener = query.stream(self.eventHandler)
    self.cache = None
    self.valueEventHandler = valueEventHandler
    self.childAddedHandler = childAddedHandler
    self.childRemovedHandler = childRemovedHandler
    self.childChangedHandler = childChangedHandler

  def close(self):
    self.listener.close()

  def eventHandler(self, event):
    print("New event:", event)
    event_type = event['event']
    event_path = event['path']
    event_data = event['data']

    if event_path == "/":
      if event_type == "put":
        self.cache = {}
      if event_data is not None:
        for key in event_data:
          self.putOrDelete(self.cache, key, event_data[key])
      if isinstance(event_data, dict):
        self.dispatchChildEvent(self.cache, event_data.keys())
    else:
      segments = list(filter(None, event_path.split("/")))
      node_kept = self.traverse(self.cache, segments, event_type, event_data)
      if len(segments) == 1 or not node_kept:
        self.dispatchChildEvent(self.cache, [segments[0]])

    if self.valueEventHandler is not None:
      self.valueEventHandler(self.cache)

  # TODO: shouldn't fire childAdded if the child already existed
  def dispatchChildEvent(self, node, keys):
    if isinstance(node, dict):
      for key in keys:
        if key in node:
          if self.childAddedHandler is not None:
            self.childAddedHandler(key, node[key])
        else:
          if self.childRemovedHandler is not None:
            self.childRemovedHandler(key)

  # Returns True if the top-level node still exists after the update
  def traverse(self, element, segments, event_type, event_data):
    if len(segments) > 1: # Path has multiple segments, traverse down
      key = segments[0]
      if not key in element:
        element[key] = {}
      self.traverse(element[key], segments[1:], event_type, event_data)
      if not element[key]: # Don't leave any empty dictionaries
        del element[key]
        return False
      else:
        return True
    else: # We're at the last segment of the path
      # TODO: need to make sure childChanged is fired if anything was changed
      key = segments[0]
      if event_type == "put":
        return self.putOrDelete(element, key, event_data)
      elif event_type == "patch":
        if not key in element:
          element[key] = {}
        for patch_key in event_data:
          return self.putOrDelete(element[key], patch_key, event_data[patch_key])

  def putOrDelete(self, element, key, data):
      if data is None:
        element.pop(key, None)
        return False
      else:
        element[key] = data
        return True
