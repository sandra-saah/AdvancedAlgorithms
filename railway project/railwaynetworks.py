from thefuzz import fuzz
from collections import defaultdict
import csv 


#### TASK 2 Class ####
""" 
  This class stores all the railway stations along with their cost, , thus, building a map of the stations
  Members:
    cost_list : Stores the cost of each edges
    adjacency_list: store edges
"""
class RailwayMap:
  def __init__(self):
    self.cost_list = {}
    self.adjacency_list = defaultdict(list)
    
  """
  Add a new element in the graph
  """
  def add_edge(self, source:str, destination:str, cost:int):
    self.adjacency_list[source].append(destination)
    self.cost_list[(source, destination)] = cost

  """
  Prints the elements in the Graph
  """
  def print_graph(self):
    for key in self.adjacency_list.keys():
      for x in range(len(self.adjacency_list[key])):
        print("Source: {0}, Destination: {1}, Cost: {2}".format(key, self.adjacency_list[key][x], self.cost_list[(key, self.adjacency_list[key][x])]  ))


#### TASK 1 Class ####
""" 
  This class stores all the railway stations data along with their code,
  Members:
    railway_stations : stores all info related to stations
    distance_graph: store a map of stations
"""
class RailwayNetwork:
 
  
  def __init__(self):
    # For Task 1
    self.railway_stations = dict() 
    # For Task 2
    self.distance_graph = RailwayMap() 
  
  ## Required for Task 1: Loads the railway_stations.csv file in form of a dictionary 
  def load_railway_stations_data(self,file_name:str):
    file = open(file_name)
    csvreader = csv.reader(file)
    header = next(csvreader)
    for data in csvreader:
      self.railway_stations[data[1]] = data[0]
  
  ## Required for Task 2: Loads the railway_newtwork.csv file in form of a graph
  def load_railway_stations_map(self,file_name:str):
    file = open(file_name)
    csvreader = csv.reader(file)
    header = next(csvreader)
    for data in csvreader:
      cost = int(data[2])
      self.distance_graph.add_edge(data[0],data[1],cost)

  ## Required for Task 1: Search through the railway_stations dictonary to find relevant results
  def search_railway_station(self, search_query:str):
    results = dict()
    found = False
    if search_query in self.railway_stations.keys():
      results[search_query] = self.railway_stations[search_query]
      found = True
    elif search_query in self.railway_stations.values():
      results[self.__get_station_code(search_query)] = search_query
      found = True
    else:
      for key in self.railway_stations.keys():
        if search_query.lower() in self.railway_stations[key].lower():
          results[key] = self.railway_stations[key]
          found = True
    if not found:
      for key in self.railway_stations.keys():
        if self.__get_similiarity_index(search_query.lower(), self.railway_stations[key].lower()) >= 0.70:
          results[key] = self.railway_stations[key]
        elif self.__get_similiarity_index(search_query.lower(), key.lower()) >= 0.70:
          results[key] = self.railway_stations[key]

    if len(results) == 0:
      results['x'] = "NOT MATCH FOUND"
    return results

   ## Required for Task 2: Search through the railway_map dictonary to find optimal path
  def search_railway_path(self, source: str, dest:str):
    shortest_paths = {source: (None, 0)}
    current_node = source
    visited = set()
    
    while current_node != dest:
        visited.add(current_node)
        destinations = self.distance_graph.adjacency_list[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = self.distance_graph.cost_list[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path


  '''
    Checks and returns
        1. The similarity index between two strings for index based searching
        2. If yes then how may words actually have the prefix
    '''
  def __get_similiarity_index(self,str1: str, str2: str):
    
    return fuzz.partial_token_sort_ratio(str1,str2)/100
    # return SequenceMatcher(None, str1, str2).ratio()

  '''
    Checks and returns
        1. The corresponding station code for a station
    '''
  def __get_station_code(self, station_name:str):
    for key in self.railway_stations.keys():
      if self.railway_stations[key] == station_name:
        return key
