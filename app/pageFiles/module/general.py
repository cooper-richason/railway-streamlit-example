import os, yaml, json, pandas as pd, shutil

def _transfer_file(from_path, to_path):
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"File not found: {from_path}")
    if os.path.exists(to_path):
        raise FileExistsError(f"File already exists: {to_path}")
    shutil.copy(from_path, to_path)

def _read_file(file_path):
    """
    Reads a file and returns its contents based on the file extension.

    Parameters
    ----------
    file_path : str
        The path to the file to be read.

    Returns
    -------
    DataFrame, dict, list, or object
        Returns a DataFrame if the file is a CSV, a dictionary if the file is JSON,
        a list of strings if the file is a text file, and a YAML object if the file
        is YAML.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the file extension is not supported.
    """
    file_extension = os.path.splitext(file_path)[1]

    if file_extension == '.csv':
        return pd.read_csv(file_path)
    
    elif file_extension == '.json':
        with open(file_path, 'r') as file:
            return json.load(file)

    elif file_extension == '.txt':
        with open(file_path, 'r') as file:
            return file.readlines()
            
    elif file_extension == '.yaml' or file_extension == '.yml':
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

def get_file(file):
    """
    Reads a file from either the local or production source based on the
    environment variables.

    Parameters
    ----------
    file : str
        The path to the file to be read, relative to the local or production
        source.

    Returns
    -------
    DataFrame, dict, list, or object
        Returns a DataFrame if the file is a CSV, a dictionary if the file is
        JSON, a list of strings if the file is a text file, and a YAML object if
        the file is YAML.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the file extension is not supported.
    """
    file_extension = os.path.splitext(file)[1]
    
    if file_extension not in ['.csv', '.json', '.txt', '.yaml', '.yml']: 
        raise ValueError(f"Unsupported file extension: {file_extension}")

    prod_path = os.path.join('/local/kick-volume/', file)
    dev_path = os.path.join('local/', file)

    if 'RAILWAY' not in os.environ or os.path.exists(prod_path) or os.environ.get('PRODUCTION_SOURCE') != 'RAILWAY':
        return _read_file(dev_path)
    elif os.path.exists(prod_path):
        return _read_file(prod_path)
    elif not os.path.exists(prod_path):
        _transfer_file(dev_path, prod_path)
        return _read_file(prod_path)

def write_file(file, data):
    """
    Writes a file to either the local or production source based on the
    environment variables.

    Parameters
    ----------
    file : str
        The path to the file to be written, relative to the local or production
        source.
    data : DataFrame, dict, list, or object
        The data to be written to the file.

    Raises
    ------
    ValueError
        If the file extension is not supported.
    """
    prod_path = os.path.join('/local/kick-volume/', file)
    dev_path = os.path.join('local/', file)
    file_extension = os.path.splitext(file)[1]

    if file_extension not in ['.csv', '.json', '.txt', '.yaml', '.yml']:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    if 'RAILWAY' not in os.environ or os.path.exists(prod_path) or os.environ.get('PRODUCTION_SOURCE') != 'RAILWAY':
        write_path = os.path.join('local/', file)
    else :
        write_path = os.path.join('/local/kick-volume/', file)

    if file_extension == '.csv':
        data.to_csv(write_path, index=False)

    elif file_extension == '.json':
        with open(write_path, 'w') as file:
            json.dump(data, file)

    elif file_extension == '.txt':
        with open(write_path, 'w') as file:
            file.write('\n'.join(data))

    elif file_extension == '.yaml' or file_extension == '.yml': 
        with open(dev_path, 'w') as file:    
            yaml.dump(data, file, default_flow_style=False)