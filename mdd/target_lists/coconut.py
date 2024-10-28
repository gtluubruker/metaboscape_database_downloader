import os
import pandas as pd
from urllib.request import urlretrieve
import zipfile


DOWNLOAD_LINK = 'https://coconut.s3.uni-jena.de/prod/downloads/2024-10/coconut_complete-10-2024.csv.zip'


def download(outdir):
    print('Downloading COCONUT')
    url = DOWNLOAD_LINK
    file_path = os.path.join(outdir, 'COCONUT.zip')
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)
    return file_path


def unzip_file(file_path):
    print('Unzipping COCONUT')
    outdir = os.path.splitext(file_path)[0]
    with zipfile.ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(outdir)
    return os.path.join(outdir, 'coconut_complete-10-2024.csv')


def convert_to_target_list(input_file, outdir, template='metaboscape_target_list_template.csv'):
    print('Converting COCONUT to MetaboScape Target List')
    template = pd.read_csv(template)
    coconut = pd.read_csv(input_file)
    template['Formula'] = coconut['molecular_formula'].values
    template['Name'] = coconut['name'].values
    template['InChI'] = coconut['standard_inchi'].values
    template.to_csv(os.path.join(outdir, 'COCONUT_MetaboScape_Target_List.csv'), index=False)
