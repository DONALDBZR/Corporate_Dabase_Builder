# For using this application, it needs to have its own virtual environment to have all of its dependencies.

```bash
python3 -m venv ./venv
```

# The virtual environment will also need to be activated for the application to be able to inject all of its dependencies.

```bash
source ./venv/bin/activate
```

# Installing the dependencies in the virtual environment files.

```bash
pip install -r requirements.txt
```

# Installing the scripts to be automated

```bash
crontab -e
```

# The first module has to be configured to be run each 15 minutes
```bash
*/15 * * * * ./venv/bin/python3 ./Auto/collect_corporate_metadata.py
```