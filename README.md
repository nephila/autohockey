Autohockey
==========
A simple script to upload a given app to HockeyApp.

Install
-------
```
# python setup.py install
```

Usage
-----
Create your config file in your working directory using json format
```
{
    "api_token": "0000F4K30000",
    "notify": 1,
}
```
Then launch
```
$ autohockey my_apk_or_ipa_or_app.zip_path --config-file my/config/path/.cfg
```
By deafult autohockey reads autohockey.cfg file in your current directory.

Instead of using a config file, you can specify your parameters from the command line, launch the helper to see all the available options
```
$ autohockey --help
```

You can also use autohockey as a module
```
import autohockey

autohockey.upload('myapp.apk', api_token='F4K3T0K3N')

```

Run tests
---------
```
# nosetests test.py
```
-------
Relased under MIT license, Copyright (c) 2014 Nephila