# Missions Finder

Missions Finder is a program that use selenium in order to scrap and search freelance missions on various website.

# Configure the virtual environment

## Create a new environment virtualenv
Create a virutal environment using [virtualenv](https://docs.python.org/fr/3/library/venv.html).

```bash
python3 -m venv venv
```

## Entering the environment

```bash
source venv/bin/activate
```

# Installation of package listed in requirement.txt

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip3 install -r requirements.txt
```

# Configure environment variables
1. Rename the file .env-example to .env
2. Put your username and password in .env file
```
USERNAME=
PASSWORD=
```

# Run the program
After having activate the virtual environment, run the program by typing in the terminal :
```bash
python3 app.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)