# Authentication and Account Management

This guide covers authentication methods and account management operations for the Datawrapper API.

## Authentication

### Using Environment Variables

The recommended way to authenticate is by setting the DATAWRAPPER_ACCESS_TOKEN environment variable. Then initialize the client without passing the token.

```python
from datawrapper import Datawrapper

dw = Datawrapper()
```

### Passing Token Directly

You can also pass the token directly when initializing:

```python
from datawrapper import Datawrapper

dw = Datawrapper(access_token="your_token_here")
```

## Account Management

### Get Account Information

Retrieve information about your Datawrapper account:

```python
account_info = dw.get_my_account()
print(f"User: {account_info['name']}")
print(f"Email: {account_info['email']}")
print(f"Role: {account_info['role']}")
```

### Get Recently Edited Charts

Retrieve your recently edited charts:

```python
recent_charts = dw.get_my_recently_edited_charts(limit=10)
for chart in recent_charts:
    print(f"{chart['id']}: {chart['title']}")
```

### Get Published Charts

Retrieve your published charts:

```python
published_charts = dw.get_my_recently_published_charts(limit=10)
for chart in published_charts:
    print(f"{chart['id']}: {chart['title']} - {chart['publicUrl']}")
