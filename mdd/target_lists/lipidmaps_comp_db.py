import os
import pandas as pd
from urllib.request import urlretrieve
import zipfile


DOWNLOAD_LINK = 'https://www.lipidmaps.org/files/store/COMP_DB_DATA.zip'


def download(outdir):
    print('Downloading LipidMaps COMP_DB')
    url = DOWNLOAD_LINK
    file_path = os.path.join(outdir, 'LipidMaps_COMP_DB.zip')
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)
    return file_path


def unzip_file(file_path):
    print('Unzipping LipidMaps COMP_DB')
    outdir = os.path.splitext(file_path)[0]
    with zipfile.ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(outdir)
    return os.path.join(outdir, 'COMP_DB_DATA.tsv')


def convert_to_target_list(input_file, outdir, template='metaboscape_target_list_template.csv'):
    print('Converting LipidMaps COMP_DB to MetaboScape Target List')
    template = pd.read_csv(template)
    comp_db = pd.read_table(input_file, sep='\t')
    template['Formula'] = comp_db['formula'].values
    template['Name'] = comp_db['abbrev'].values
    template.to_csv(os.path.join(outdir, 'LipidMaps_COMP_DB_MetaboScape_Target_List.csv'), index=False)
