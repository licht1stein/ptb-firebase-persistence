![](https://github.com/python-telegram-bot/logos/blob/master/logo/png/ptb-logo_240.png?raw=true)
# Firebase Persistence for [python-telegram-bot](https://python-telegram-bot.org/)

This is an implementation of python-telegram-bot [BasePersistence](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.basepersistence.html?highlight=basepersistence) 
class that uses [Google Firebase](https://firebase.google.com/) as persistence back-end. 
This has a very nice advantage of being able to look at your `user_data`, `chat_data`, `bot_data` 
and `convesations` real-time using the firebase web app.

# Installation


# Usage

## Before you start: obtain credentials from firebase
First of all you need to obtain firebase credentials, that look like this:

```json
{
  "type": "service_account",
  "project_id": "YOUR_ID",
  "private_key_id": "YOUR_PRIVATE_KEY",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMII...EwQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-odh1e@SOME_DOMAIN.iam.gserviceaccount.com",
  "client_id": "11743776666698009",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-SOMES_STRING.iam.gserviceaccount.com"
}
```

and the firebase database url that looks like this, something like `https://YOUR_APP.firebaseio.com`

## Instantiation

### From environment variables (recommended)
Store the database URL in an environment variable `FIREBASE_URL` and the config as a json string in an environment variable
`FIREBASE_CREDENTIALS`.

After that instantiation is as easy as:

```python
from ptb_firebase_persistence import FirebasePersistence
from telegram.ext import Updater


persistence = FirebasePersistence.from_environment()

updater: Updater = Updater(
    'BOT_TOKEN',
    persistence=my_persistence,
    use_context=True,
)
```

### Direct instantiation
You can also just pass the firebase credentials as URL as simple init params:

```python
from ptb_firebase_persistence import FirebasePersistence
from telegram.ext import Updater


persistence = FirebasePersistence(database_url='YOUR_DATABASE_URL', credentials='YOUR_CREDENTIALS_DICT')

updater: Updater = Updater(
    'BOT_TOKEN',
    persistence=my_persistence,
    use_context=True,
)
```
