import os
import time
import numpy as np
import pandas as pd
from urllib.request import urlretrieve
import pubchempy as pcp


DOWNLOAD_LINK = 'https://figshare.com/ndownloader/files/18130628'


def download(outdir):
    print('Downloading METLIN SMRT')
    url = DOWNLOAD_LINK
    file_path = os.path.join(outdir, 'METLIN_SMRT.csv')
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)
    return file_path


def convert_to_target_list(input_file, outdir, template='metaboscape_target_list_template.csv'):
    print('Converting METLIN SMRT to MetaboScape Target List')
    template = pd.read_csv(template)
    metlin_smrt = pd.read_table(input_file, sep=';')

    def get_compound_info_from_pcp(cid):
        time.sleep(0.25)
        return pcp.Compound.from_cid(cid)

    compounds = [get_compound_info_from_pcp(i) for i in metlin_smrt['pubchem']]
    template['RT'] = metlin_smrt['"rt"']
    template['Formula'] = np.array([i.molecular_formula for i in compounds])
    template['Name'] = np.array([i.iupac_name for i in compounds])
    template['InChI'] = np.array([i.inchi for i in compounds])
    template['PubChem'] = metlin_smrt['pubchem'].values
    template.to_csv(os.path.join(outdir, 'METLIN_SMRT_MetaboScape_Target_List.csv'), index=False)
