# Organization

Managing organizational structures in Datawrapper, including folders, themes, and team workspaces.

## Folders

### List Folders

Get all folders in your account:

```python
folders = client.get_folders()
for folder in folders:
    print(f"{folder['id']}: {folder['name']}")
```

### Create a Folder

Create a new folder:

```python
folder = client.create_folder(name="Q4 2024 Reports")
folder_id = folder['id']
```

### Move Chart to Folder

Move a chart to a specific folder:

```python
client.move_chart(chart_id="abc123", folder_id=folder_id)
```

## Themes

### List Available Themes

Get all themes available to your account:

```python
themes = client.get_themes()
for theme in themes:
    print(f"{theme['id']}: {theme['title']}")
```

### Apply Theme to Chart

Apply a theme when creating or updating a chart:

```python
import datawrapper as dw

chart = dw.BarChart(
    title="Themed Chart",
    data=df,
    theme="my-custom-theme"
)
chart_id = chart.create()
```

## Teams and Workspaces

### Get Team Information

If you're part of a team, retrieve team information:

```python
teams = client.get_teams()
for team in teams:
    print(f"{team['id']}: {team['name']}")
```

### Get Team Settings

Get settings for a specific team:

```python
team_settings = client.get_team_settings(team_id="team123")
```
