<!--
    DO NOT MANUALLY EDIT THIS FILE
    THIS FILE IS AUTOMATICALLY GENERATED WITH resilient-circuits codegen
-->

# Example: LDAP MultiDomain Utilities: Add User/s to Group/s

## Function - LDAP MultiDomain Utilities: Add to Group(s)

### API Name
`ldap_md_utilities_add_to_groups`

### Output Name
`None`

### Message Destination
`fn_ldap_md_utilities`

### Pre-Processing Script
```python
# Both inputs must be a string representation of a List

## Example of multiple entries
# inputs.ldap_multiple_user_dn = "['dn=user1,dc=example,dc=com', 'dn=user2,dc=example,dc=com']"
# inputs.ldap_multiple_group_dn = "['dn=Accounts Group,dc=example,dc=com', 'dn=IT Group,dc=example,dc=com']"

## Note: You can use this handy function below, then not need to worry about the inputs formatting

def into_string_list_format(entries):
  """Function that converts a list or single string into a 'string repersentation of a list'"""
  string_list_to_return = "[{0}]"
  
  # If its a string, assume its one DN, one entry
  if isinstance(entries, basestring):
    return string_list_to_return.format('"{0}"'.format(entries))
  
  # Else assume its a List, so multiple DNs, multiple entries
  else:
    entries_to_add = ""
    for e in entries:
      entries_to_add += '"{0}",'.format(e)
    return string_list_to_return.format(entries_to_add)

list_of_users_dn = ['dn=user1,dc=example,dc=com', 'dn=user2,dc=example,dc=com']

# Both inputs must be a string representation of a List
inputs.ldap_multiple_user_dn = into_string_list_format(list_of_users_dn)
inputs.ldap_multiple_group_dn = into_string_list_format('dn=Accounts Group,dc=example,dc=com')
```

### Post-Processing Script
```python
# If the function is successful in adding the users to said groups,
# a note is added to the incident

if (results.success):
  noteText = """<br><i style="color: #979ca3">LDAP Utilities: Add User(s) to Group(s) <u>complete</u>:</i>
                    <b>User(s):</b> {0}
                    <b>Group(s):</b> {1}""".format(results.users_dn, results.groups_dn)
  
  incident.addNote(helper.createRichText(noteText))
```

---
