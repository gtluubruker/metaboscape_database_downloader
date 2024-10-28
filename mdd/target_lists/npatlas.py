import os
import pandas as pd
from urllib.request import urlretrieve, build_opener, install_opener


DOWNLOAD_LINK = 'https://www.npatlas.org/static/downloads/NPAtlas_download.tsv'


def download(outdir):
    print('Downloading NPAtlas')
    url = DOWNLOAD_LINK
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    install_opener(opener)
    file_path = os.path.join(outdir, 'NPAtlas_download.tsv')
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)
    return file_path


def convert_to_target_list(input_file, outdir, template='metaboscape_target_list_template.csv'):
    print('Converting NPAtlas to MetaboScape Target List')
    template = pd.read_csv(template)
    npatlas = pd.read_table(input_file, sep='\t')
    template['Formula'] = npatlas['compound_molecular_formula'].values
    template['Name'] = npatlas['compound_name'].values
    template['InChI'] = npatlas['compound_inchi'].values
    template.to_csv(os.path.join(outdir, 'NPAtlas_MetaboScape_Target_List.csv'), index=False)
