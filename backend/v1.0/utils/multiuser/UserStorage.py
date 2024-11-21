import json
import os

current_folder = os.getcwd()
users_folder = os.path.join(current_folder,"v1.0", "users", "users.json")

class multiuserstorage:
    def __init__(self, user, instance):
      self.user = user
      self.instance = instance

    def storageUser (self):
      try:
        with open(users_folder, "r") as json_file:
            data = json.load(json_file)

        if self.user in data:
            del data[self.user]
        user_data = self.instance.to_dict()
        data[self.user] = user_data

        with open(users_folder, "w") as json_file:
            json.dump(data, json_file, indent=4)

      except FileNotFoundError:
         print(f'Error: File{users_folder} not found.')
      except json.JSONDecodeError:
         print(f"Error: File '{users_folder}' is not a valid JSON file.")
      

         

    
       


        