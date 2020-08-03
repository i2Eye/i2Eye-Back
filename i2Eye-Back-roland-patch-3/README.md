# i2Eye-Back
The backend of i2Eye uses the following:
1. Python 3.8.1 (https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe)
2. Flask - A web app framework running on python (https://github.com/pallets/flask)
3. ElasticSearch - HTTP search engine (https://www.elastic.co/downloads/elasticsearch)
4. Conda - Virtual Environment Manager for managing dependencies (https://docs.anaconda.com/anaconda/install/)

## How to Setup the Back-end Environment
Step 1: Install Anaconda, so that depencencies in Python can be seperately managed (skip this step if you already have a virtual environment manager)

Step 2: After installation, run Anaconda Prompt and create the virtual environment for i2eye using the following commands:
```
conda update --all
conda create --name i2eye python=3.8.1 flask=1.1.2 ... (all other packages on requirements.txt)
```
Step 3: Some packages are not found in the standard Anaconda repository i.e elasticsearch v7.6.0, Flask-cors v3.0.8. Install them using the conda-forge repository: 
```
conda install -c conda-forge elasticsearch=7.6.0 elasticsearch-dsl Flask-cors=3.0.8 ... (other dependencies)
``` 

This will create our python virtual environment with flask and elasticsearch. Then, activate the environment using:
```
conda activate i2eye
```
The environment is now set-up. To run your python scripts, run `python your_code.py` within Anaconda Prompt.
For more useful Anaconda commands, refer to the cheatsheet at https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf
