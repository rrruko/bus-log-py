import json
import operator
import math

from .geo import Segment, Point, Polyline
from .haversine import haversine

# Parse shape.json into a map where keys are shape ids and values are the
# shapes represented as Polylines.
def enumerate_shapes(trips_json, shape_json):
  shapes = {}
  shape_to_route = {}
  for trip in trips_json:
    if trip["shape_id"] in shape_to_route:
      if not shape_to_route[trip["shape_id"]] == trip["route_id"]:
        raise ValueError
    else:
      shape_to_route[trip["shape_id"]] = trip["route_id"]
  for shape in shape_json:
    point = Point(shape["shape_pt_lat"], shape["shape_pt_lon"])
    shape_id = shape["shape_id"]
    route_id = shape_to_route[shape_id]
    shapes.setdefault((shape_id, route_id), Polyline([])).points.append(point)
  return shapes

# Get the route that has the closest segment. This is likely to be the route
# that the bus is on.
def guess_route(shapes, bus_record):
  closest_so_far = None
  closest_shape_key = None
  for shape_key, shape in shapes.items():
    # TODO: This shouldn't be handled here; this function shouldn't accept
    # invalid buses
    try:
      bus_point = Point(
        float(bus_record["latitude"]),
        float(bus_record["longitude"]))
    except ValueError as v:
      # Sometimes the bus won't have a valid lat/lon, so we'll just ignore it
      continue
    closest_seg = shape.closest_segment(bus_point)
    if closest_so_far is None:
      closest_so_far = closest_seg
      closest_shape_key = shape_key
    elif closest_seg.distance_to(bus_point) < closest_so_far.distance_to(bus_point):
      closest_so_far = closest_seg
      closest_shape_key = shape_key
  return closest_shape_key

def mean(xs):
  return sum(xs) / len(xs)

def route_histo(shapes, bus_history):
  shapes_histo = {}
  for bus_point in bus_history:
    for shape_id, shape in shapes.items():
      closest_seg, distance = shape.closest_segment(bus_point, get_distance=True)
      if shape_id in shapes_histo:
        shapes_histo[shape_id].append(distance)
      else:
        shapes_histo[shape_id] = [distance]
  return [(shape, mean(distances)) for shape, distances in shapes_histo.items()]

def passes(bus_history, bus_stop, route, max_dist=None):
  sign = None
  for observation in bus_history:
    dist = route.distance_along(bus_stop) - route.distance_along(observation)
    geodesic_dist = haversine(bus_stop, observation)
    if max_dist and geodesic_dist > max_dist:
      return False
    if sign is not None and sign != math.copysign(1, dist):
      return True
    sign = math.copysign(1, dist)
  return False
