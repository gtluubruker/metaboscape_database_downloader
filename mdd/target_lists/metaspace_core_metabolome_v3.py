import os
import pandas as pd
from urllib.request import urlretrieve


DOWNLOAD_LINK = 'https://s3-eu-west-1.amazonaws.com/sm-mol-db/db_files_2021/core_metabolome/core_metabolome_v3.csv'


def download(outdir):
    print('Downloading METASPACE Core Metabolome v3')
    url = DOWNLOAD_LINK
    file_path = os.path.join(outdir, 'METASPACE_Core_Metabolome_v3.tsv')
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)
    return file_path


def convert_to_target_list(input_file, outdir, template='metaboscape_target_list_template.csv'):
    print('Converting METASPACE Core Metabolome v3 to MetaboScape Target List')
    template = pd.read_csv(template)
    core_metabolome_v3 = pd.read_table(input_file, sep='\t')
    template['Formula'] = core_metabolome_v3['formula'].values
    template['Name'] = core_metabolome_v3['name'].values
    template['InChI'] = core_metabolome_v3['inchi'].values
    template.to_csv(os.path.join(outdir, 'METASPACE_Core_Metabolome_v3_MetaboScape_Target_List.csv'), index=False)
