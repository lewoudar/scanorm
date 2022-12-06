# scanorm

A re-utilisable django package which scans a Django project and creates a JSON file called `.forestadmin-schema.json` in
the root directory with all the models discovered in the project.

## Installation

This library works with python version >=3.9 and Django version >= 4.X.

## Usage

Declare the app `scanorm` in `INSTALLED_APPS`.

The file will have the following form:

```json
{
  "scanorm": null,
  "django.contrib.admin": {
    "ContentType": {
      "logentry": "ManyToOneRel",
      "permission": "ManyToOneRel",
      "id": "AutoField",
      "app_label": "CharField",
      "model": "CharField"
    },
    "LogEntry": {
      "id": "AutoField",
      "action_time": "DateTimeField",
      "user": "ForeignKey",
      "content_type": "ForeignKey",
      "object_id": "TextField",
      "object_repr": "CharField",
      "action_flag": "PositiveSmallIntegerField",
      "change_message": "TextField"
    }
  },
  ...
}
```

When an app does not have models or the library can't detect them, the value will be None. Otherwise, you will have
for each app, a dictionary of models, and for each model its list of fields with its type.
