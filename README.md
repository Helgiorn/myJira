# jira-issue-creator
Very basic command line tool that manages som simple day to day tasks in JIRA.

## Usage
```
python ./my_jira.py --help
```

## Requirements
```console
pip install pywin32
pip install keyring
pip install jira
pip install argparse
```

### Credential Manager
This is a decent way to keep your credentials away from your code, open "Credential Manager" in windows to manage saved profiles. 

```python
import keyring

keyring.set_password("jria-api", "user", "password")
password = keyring.get_password("servicejira", "user")
print (password)
```

