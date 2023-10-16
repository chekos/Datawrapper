from pprint import pprint
from datawrapper import Datawrapper

dw = Datawrapper()

# Get a randoms string suffix to use in our names
import random
import string

suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

dw = Datawrapper()

# Create a team
team = dw.create_team("Test Team", id="test-team")
assert isinstance(team, dict)
pprint(team)

# Get the team
# team = dw.get_team(team["id"])
# pprint(team)

# # Update the team
# team = dw.update_team(team["id"], "Test Team 2")
# pprint(team)

# # Get the team again
# team = dw.get_team(team["id"])
# pprint(team)

# # Verify that the name changed
# assert team["name"] == "Test Team 2"

# # Delete the team
# dw.delete_team(team["id"])

# # Verify that if you try to get this team it will now raise an exception
# with pytest.raises(Exception):
#     dw.get_team(team["id"])

# themes = dw.get_themes(offset=2, limit=1)
# pprint(themes)

# recent_charts = dw.get_my_recently_published_charts(limit=1)
# pprint(recent_charts)

# # Get account info
# account_info = dw.get_my_account()
# pprint(account_info)

# account_info = dw.update_my_account(name="Foobar")
# pprint(account_info)

# account_info = dw.get_my_account()
# pprint(account_info)

# account_info = dw.update_my_account(name="Ben Welsh")
# pprint(account_info)

# account_info = dw.get_my_account()
# pprint(account_info)

# Get the iowa-counties basemap
# basemap_key = dw.get_basemap_key("iowa-counties", 'GEOID')
# pprint(basemap_key)

# Get list of basemaps
# basemaps = dw.get_basemaps()
# pprint(basemaps)

# # Create a new folder
# folder_info = dw.create_folder(name="My new folder" + suffix)

# # Get the folder's data with a fresh get_folder call
# folder_info = dw.get_folder(folder_info["id"])

# # Make a second folder
# second_folder_info = dw.create_folder(name="My second folder" + suffix)

# # Move the second folder into the first folder
# dw.update_folder(
#     folder_id=second_folder_info["id"], parent_id=folder_info["id"]
# )

# # Get the folder's data with a fresh get_folder call
# second_folder_info = dw.get_folder(second_folder_info["id"])

# # Verify it has the parent
# assert second_folder_info["parentId"] == folder_info["id"]

# # Change the name of the second folder
# dw.update_folder(folder_id=second_folder_info["id"], name="My second folder (renamed)")

# # Get it fresh and verify the change
# second_folder_info = dw.get_folder(second_folder_info["id"])
# assert second_folder_info["name"] == "My second folder (renamed)"

# # Delete both folders
# dw.delete_folder(folder_info["id"])

# # Verify that you can't get either using assertRaises
# # with pytest.raises(Exception):
# try:
#     dw.get_folder(folder_id=folder_info["id"])
# except Exception as e:
#     print("Good")

# try:
#     dw.get_folder(folder_id=second_folder_info["id"])
# except Exception as e:
#     print("Good")
