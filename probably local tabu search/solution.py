import json

class Solution:

    def __init__(self, filename = None):
        
        
        with open('sol.json','r') as file:
            sol = json.load(file)

        print(sol)