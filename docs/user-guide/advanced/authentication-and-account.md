# Authentication and Account Management

Lower-level authentication methods and account management operations for the Datawrapper API. Not necessary to create charts with our object-oriented models, but useful for advanced users.

## Authentication

### Using Environment Variables

The recommended way to authenticate is by setting the DATAWRAPPER_ACCESS_TOKEN environment variable. Then initialize the client without passing the token.

```python
import datawrapper as dw

client = dw.Datawrapper()
```

### Passing Token Directly

You can also pass the token directly when initializing:

```python
client = dw.Datawrapper(access_token="your_token_here")
```

## Account Management

### Get Account Information

Retrieve information about your Datawrapper account:

```python
account_info = client.get_my_account()
print(f"User: {account_info['name']}")
print(f"Email: {account_info['email']}")
print(f"Role: {account_info['role']}")
```

### Get Recently Edited Charts

Retrieve your recently edited charts:

```python
recent_charts = client.get_my_recently_edited_charts(limit=10)
for chart in recent_charts:
    print(f"{chart['id']}: {chart['title']}")
```

### Get Published Charts

Retrieve your published charts:

```python
published_charts = client.get_my_recently_published_charts(limit=10)
for chart in published_charts:
    print(f"{chart['id']}: {chart['title']} - {chart['publicUrl']}")
```
