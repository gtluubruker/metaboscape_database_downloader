import os
import pandas as pd
from urllib.request import urlretrieve


DOWNLOAD_LINK = 'https://s3-eu-west-1.amazonaws.com/sm-mol-db/db_files_2021/nglyc/nglyc_v1.tsv'


def download(outdir):
    print('Downloading METASPACE NGlycDB')
    url = DOWNLOAD_LINK
    file_path = os.path.join(outdir, 'METASPACE_NGlycDB.tsv')
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)
    return file_path


def convert_to_target_list(input_file, outdir, template='metaboscape_target_list_template.csv'):
    print('Converting METASPACE NGlycDB to MetaboScape Target List')
    template = pd.read_csv(template)
    nglycdb = pd.read_table(input_file, sep='\t')
    template['Formula'] = nglycdb['formula'].values
    template['Name'] = nglycdb['name'].values
    template.to_csv(os.path.join(outdir, 'METASPACE_NGlycDB_MetaboScape_Target_List.csv'), index=False)
