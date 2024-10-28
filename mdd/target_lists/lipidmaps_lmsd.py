import os
from urllib.request import urlretrieve
import zipfile
import pandas as pd
from rdkit.Chem import SDMolSupplier


DOWNLOAD_LINK = 'https://www.lipidmaps.org/files/?file=LMSD&ext=sdf.zip'


def download(outdir):
    print('Downloading LipidMaps LMSD')
    url = DOWNLOAD_LINK
    file_path = os.path.join(outdir, 'LipidMaps_LMSD.zip')
    if not os.path.isfile(file_path):
        urlretrieve(url, file_path)
    return file_path


def unzip_file(file_path):
    print('Unzipping LipidMaps LMSD')
    outdir = os.path.splitext(file_path)[0]
    with zipfile.ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(outdir)
    return os.path.join(outdir, 'structures.sdf')


def convert_to_target_list(input_file, outdir):
    print('Converting LipidMaps LMSD to MetaboScape Target List')
    # Read in SDF file.
    suppl = SDMolSupplier(input_file)

    molecular_properties = []
    count = 1
    # Loop through molecules from the SDF file.
    for mol in suppl:
        if count % 10000 == 0:
            print('Finished Processing Molecule ' + str(count))
        # Get property names and place them into dict.
        mol_props = mol.GetPropNames()
        mol_props_dict = {}
        for prop in mol_props:
            mol_props_dict[prop] = mol.GetProp(prop)
        # Initialize dict for MetaboScape Target List format.
        mol_props_dict2 = {'RT': '',
                           'Formula': mol_props_dict['FORMULA'],
                           'Name': '',
                           'CCS [M+H]+': '',
                           'CCS [M+Na]+': '',
                           'CCS [M-H]-': '',
                           'KEGG': '',
                           'CAS': '',
                           'PubChem': '',
                           'ChemSpider': '',
                           'HMDB': '',
                           'BioCyc': '',
                           'Metlin': '',
                           'LipidMaps': mol_props_dict['LM_ID'],
                           'UserID': '',
                           'InChI': mol_props_dict['INCHI']}
        # Assign compound names based on presence/absence of name/systematic name/abbreviation.
        if 'NAME' in mol_props_dict.keys():
            if 'ABBREVIATION' in mol_props_dict.keys():
                mol_props_dict2['Name'] = mol_props_dict['NAME'] + ' | ' + mol_props_dict['ABBREVIATION']
            else:
                mol_props_dict2['Name'] = mol_props_dict['NAME']
        elif 'SYSTEMATIC_NAME' in mol_props_dict.keys():
            if 'ABBREVIATION' in mol_props_dict.keys():
                mol_props_dict2['Name'] = mol_props_dict['SYSTEMATIC_NAME'] + ' | ' + mol_props_dict['ABBREVIATION']
            else:
                mol_props_dict2['Name'] = mol_props_dict['SYSTEMATIC_NAME']
        else:
            mol_props_dict2['Name'] = mol_props_dict['LM_ID']
        # Add PubChem ID if present.
        if 'PUBCHEM_CID' in mol_props_dict.keys():
            mol_props_dict2['PubChem'] = mol_props_dict['PUBCHEM_CID']
        molecular_properties.append(mol_props_dict2)
        count += 1

    # Write to target list format CSV file.
    target_list = pd.DataFrame(molecular_properties)
    target_list.to_csv(os.path.join(outdir, 'LipidMaps_LMSD_MetaboScape_Target_List.csv'), index=False)
