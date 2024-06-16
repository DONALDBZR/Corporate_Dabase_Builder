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

# The scripts cannot be run headless as there is Google Analytics on the host which will detect the crawler if it is headless.  Besides, the first script which will execute for a total duration of fifteen minutes which can be executed as follows.

```bash
sh /home/admin/Documents/Darkness4869/fincorp/Auto/collect_corporate_metadata.py
```