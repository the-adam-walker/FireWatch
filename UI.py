##############################
#  UI for FireWatch Project  #
##############################

from tabulate import tabulate

#passed in data for name(?), distance, and heading
#placeholder examples
moduleNames = ('NodeA', 'NodeB', 'NodeC')
distance = ('13m', '7m', '12m')
direction = (heading1, heading2, heading3)


table = [[moduleNames[0], distance[0], direction[0]],
         [moduleNames[1], distance[1], direction[1]],
         [moduleNames[2], distance[2], direction[2]]]

headers = ["Name", "Distance", "Direction"]

print(tabulate(table, headers))
