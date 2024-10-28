import os
from urllib.request import urlretrieve


DOWNLOAD_LINK = 'https://github.com/McLeanResearchGroup/CCS-Compendium/raw/refs/heads/master/PCDL/CCS-Compendium_20211015.cdb'


def download(outdir):
    url = DOWNLOAD_LINK
    file_path = os.path.join(outdir, 'CCS-Compendium_20211015.cdb')
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)
    return file_path


def convert_to_target_list(input_file, outdir, template='metaboscape_target_list_template.csv'):
    print('Unified CCS Compendium support is currently under construction')
