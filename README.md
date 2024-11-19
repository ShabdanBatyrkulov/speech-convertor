# Create virtual environment
Enter repository
```bash
python3 -m venv .venv
```

# Activate a virtial environment
Before you can start installing or using packages in your virtual environment you’ll need to `activate` it. Activating a virtual environment will put the virtual environment-specific `python` and `pip` executables into your shell’s `PATH`.
```bash
source .venv/bin/activate
```

To confirm the virtual environment is activated, check the location of your Python interpreter:
```bash
which python
```

While the virtual environment is active, the above command will output a filepath that includes the `.venv` directory, by ending with the following:
```bash
.venv/bin/python
```

# Prepare dependencies

```bash
python3 -m pip install -r requirements.txt
```

# Run the program
```
python3 main.py
```

# Deactivate a virtual environment
If you want to switch projects or leave your virtual environment, `deactivate` the environment:
```bash
deactivate
```
