Application made and tested in  `Debian 11`

## Set up a python virtual enviroment.
I used dirnev to manage virtual environments.
To install it:
```
sudo apt install direnv
```
after installing enable it using:
```
direnv allow
```
## Prerequisite:
First go into its director:
```
cd TodoApp
```
Install this package in edit mode using:
```
TodoApp$ pip install -e .[dev]
```
`dev` is optional as it installs `pylint`

### Start the API Server:
```
TodoApp$ python -m TodoApp
```

## Decrypting response
The response is returned as json. The values are encrypted using `cryptography`.

The key is kept static. which is `b'YXQVEB5f_Pulby5C4LZ19R6GHqZby6DqRK9eBN779wg='`

    Steps:
```
$ python
>>> from cryptography.fernet import Fernet
>>> f = Fernet(b'YXQVEB5f_Pulby5C4LZ19R6GHqZby6DqRK9eBN779wg=')
```

then use the `val` that you want to decrypt:
```
>>>f.decrypt("string value in response to be decrypted".encode('utf-8')).decode('utf-8')
```
The returned value will be in string.
