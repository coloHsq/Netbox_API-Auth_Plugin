# Netbox API authentication plugin

This plugin adds two API endpoints for encrypted users authentication.

The first endpoint, **https://netbox.foo.bar/api/plugins/auth/key-exchange/**, is used for keys exchange.  
A client that use this login system must first POST a public RSA key ( _RSA/ECB/OAEPwithSHA-256andMGF1Padding_ ) 
to this endpoint, subsequently AES key and nonce will be generated, temporarily cached to Redis, RSA encrypted and 
finally sent back in response with a session id.

The second endpoint **https://netbox.foo.bar/api/plugins/auth/api-login/**, is used to actually perform the login.  
With data retrieved (and decrypted) from the first call, AES key, nonce ( _AES/GCM/NoPadding_ ) and session id, 
a client have to encrypt user credentials and expiration date to then POST them with the session id, 
to finally receive in response the auth Token.

All the cryptography is meant to be "one time encryption" as no key is permanently saved.

## Installation and configuration
1. Download this repo and place it under "/opt/netbox/netbox/" (along with other django apps).
2. Add `'auth_api'` to `PLUGINS` under "/opt/netbox/netbox/netbox/configuration.py".
3. Add `'auth_api': {'cache_timeout': 30}` to `PLUGINS_CONFIG` under "/opt/netbox/netbox/netbox/configuration.py".
4. Create or edit 'local_requirements.txt' under "/opt/netbox" and add '-e /opt/netbox/netbox/auth-api'
5. Run '/opt/netbox/upgrade.sh' and then restart Netbox service
6. Everything should be up n' running.

## How to:

### Step 1 : POST request to /key-exchange/
**Payload :**
```
{
    "public_key": "your_rsa_public_key"
}
```

**Response from /key-exchange/ :**
```
{
    "session_id": "server_generated_session_id",
    "encrypted_data": "RSA encrypted string"
}
```

**Once decrypted, "encrypted_data" will result in a json object containing the AES key and it's nonce :**
```
{
    "key": "server_generated_aes_key",
    "nonce_iv": "server_generated_aes_nonce"
}
```

### Step 2 : Post Request to /api-login/
**Create a json object containing username, password and expiration date for the token :**
```
{
    "user": "fooUser,
    "password: "baz_password",
    "expires": "yyyy-MM-dd"
}
```

**Encrypt it with AES key and nonce retrieved in step 1 and put it in the POST request payload with the
session id :**
```
{
    "encrypted_data": "encrypted user json",
    "session_id" "step 1 retrieved session id"
}
```

**Response from /api-login/ :**
```
{
    "token": "finally_the_auth_token"
}
```
