import os
from urllib.request import urlretrieve
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from mdd.spectral_libraries import gnps, mona, msdial
from mdd.target_lists import (coconut, lipidmaps_comp_db, lipidmaps_lmsd, metaspace_core_metabolome_v3,
                              metaspace_nglycdb, metlin, npatlas, unified_ccs_compendium)

VERSION = '0.1.0'


def get_db_names():
    gnps_names = [f'SL|{i}' for i in gnps.DOWNLOAD_LINKS.keys()]
    mona_names = [f'SL|{i}' for i in mona.DOWNLOAD_LINKS.keys()]
    msdial_names = [f'SL|{i}' for i in msdial.DOWNLOAD_LINKS.keys()]
    target_list_names = ['TL|COCONUT',
                         'TL|LipidMaps_COMP_DB',
                         'TL|LipidMaps_LMSD',
                         'TL|METASPACE_Core_Metabolome_v3',
                         'TL|METASPACE_NGlycDB',
                         'TL|METLIN_SMRT',
                         'TL|NPAtlas',
                         'TL|Unified_CCS_Compendium']
    return gnps_names + mona_names + msdial_names + target_list_names


def main():
    window = tk.Tk()
    window.title(f'MetaboScape Database Downloader {VERSION}')
    window.geometry('640x150')  # Fixed size of the window

    frame = tk.Frame(window)
    frame.pack(expand=True, fill=tk.BOTH)  # Center the frame in the window

    combo = ttk.Combobox(window, values=get_db_names())
    combo.pack(padx=20, pady=5, fill=tk.X)
    combo['state'] = 'readonly'

    source = tk.Label(window, text='', fg='blue', cursor='hand2')
    source.pack(pady=5)

    def download_database():
        db_name = combo.get()
        outdir = askdirectory(mustexist=True).replace('/', '\\')
        if db_name.startswith('SL'):
            sl_download_links = {key: value
                                 for link_dict in [gnps.DOWNLOAD_LINKS,
                                                   mona.DOWNLOAD_LINKS,
                                                   msdial.DOWNLOAD_LINKS]
                                 for key, value in link_dict.items()}
            db_name = '|'.join(db_name.split('|')[1:])
            url = sl_download_links[db_name]
            file_path = os.path.join(outdir, f'{db_name}.msp')
            if not os.path.isfile(file_path):
                urlretrieve(url, file_path)
        elif db_name == 'TL|COCONUT':
            coconut_file_path = coconut.download(outdir)
            coconut_input_file = coconut.unzip_file(coconut_file_path)
            coconut.convert_to_target_list(coconut_input_file, outdir,
                                           template='target_lists/metaboscape_target_list_template.csv')
        elif db_name == 'TL|LipidMaps_COMP_DB':
            comp_db_file_path = lipidmaps_comp_db.download(outdir)
            comp_db_input_file = lipidmaps_comp_db.unzip_file(comp_db_file_path)
            lipidmaps_comp_db.convert_to_target_list(comp_db_input_file, outdir,
                                                     template='target_lists/metaboscape_target_list_template.csv')
        elif db_name == 'TL|LipidMaps_LMSD':
            lmsd_file_path = lipidmaps_lmsd.download(outdir)
            lmsd_input_file = lipidmaps_lmsd.unzip_file(lmsd_file_path)
            lipidmaps_lmsd.convert_to_target_list(lmsd_input_file, outdir)
        elif db_name == 'TL|METASPACE_Core_Metabolome_v3':
            core_metabolome_v3_input_file = metaspace_core_metabolome_v3.download(outdir)
            metaspace_core_metabolome_v3.convert_to_target_list(core_metabolome_v3_input_file, outdir,
                                                                template='target_lists/metaboscape_target_list_template.csv')
        elif db_name == 'TL|METASPACE_NGlycDB':
            nglycdb_input_file = metaspace_nglycdb.download(outdir)
            metaspace_nglycdb.convert_to_target_list(nglycdb_input_file, outdir,
                                                     template='target_lists/metaboscape_target_list_template.csv')
        elif db_name == 'TL|METLIN_SMRT':
            print('Warning: METLIN SMRT conversion can take upwards of 6 hours due to reliance on the PubChem API '
                  'which has bandwith limits.')
            metlin_input_file = metlin.download(outdir)
            metlin.convert_to_target_list(metlin_input_file, outdir,
                                          template='target_lists/metaboscape_target_list_template.csv')
        elif db_name == 'TL|NPAtlas':
            npatlas_input_file = npatlas.download(outdir)
            npatlas.convert_to_target_list(npatlas_input_file, outdir,
                                           template='target_lists/metaboscape_target_list_template.csv')
        elif db_name == 'TL|Unified_CCS_Compendium':
            print('Unified CCS Compendium support is currently under construction')

    download_button = tk.Button(window, text='Download', command=download_database)
    download_button.pack(pady=20)

    def update_source(event):
        db_name = combo.get()
        db_name = '|'.join(db_name.split('|')[1:])
        if db_name.startswith('ALL') or db_name.startswith('GNPS'):
            source.config(text='https://external.gnps2.org/gnpslibrary', fg='blue', cursor='hand2')
        elif db_name.startswith('MassBank') or db_name.startswith('MoNA'):
            source.config(text='https://mona.fiehnlab.ucdavis.edu/downloads', fg='blue', cursor='hand2')
        elif db_name.startswith('MS-DIAL'):
            source.config(text='https://systemsomicslab.github.io/compms/msdial/main.html#MSP',
                          fg='blue', cursor='hand2')
        elif db_name == 'COCONUT':
            source.config(text='https://coconut.naturalproducts.net/download', fg='blue', cursor='hand2')
        elif db_name == 'LipidMaps_COMP_DB':
            source.config(text='https://www.lipidmaps.org/databases/comp_db/download', fg='blue', cursor='hand2')
        elif db_name == 'LipidMaps_LMSD':
            source.config(text='https://www.lipidmaps.org/databases/lmsd/download', fg='blue', cursor='hand2')
        elif db_name == 'METASPACE_Core_Metabolome_v3':
            source.config(text='https://metaspace2020.eu/help', fg='blue', cursor='hand2')
        elif db_name == 'METASPACE_NGlycDB':
            source.config(text='https://metaspace2020.eu/help', fg='blue', cursor='hand2')
        elif db_name == 'METLIN_SMRT':
            source.config(text='https://figshare.com/articles/dataset/The_METLIN_small_molecule_dataset_for_machine_learning-based_retention_time_prediction/8038913',
                          fg='blue', cursor='hand2')
        elif db_name == 'NPAtlas':
            source.config(text='https://www.npatlas.org/download', fg='blue', cursor='hand2')
        elif db_name == 'Unified_CCS_Compendium':
            source.config(text='https://github.com/McLeanResearchGroup/CCS-Compendium/tree/master/PCDL',
                          fg='blue', cursor='hand2')

    combo.bind("<<ComboboxSelected>>", update_source)

    def open_source(event):
        db_name = combo.get()
        db_name = '|'.join(db_name.split('|')[1:])
        if db_name.startswith('ALL') or db_name.startswith('GNPS'):
            webbrowser.open_new_tab('https://external.gnps2.org/gnpslibrary')
        elif db_name.startswith('MassBank') or db_name.startswith('MoNA'):
            webbrowser.open_new_tab('https://mona.fiehnlab.ucdavis.edu/downloads')
        elif db_name.startswith('MS-DIAL'):
            webbrowser.open_new_tab('https://systemsomicslab.github.io/compms/msdial/main.html#MSP')
        elif db_name == 'COCONUT':
            webbrowser.open_new_tab('https://coconut.naturalproducts.net/download')
        elif db_name == 'LipidMaps_COMP_DB':
            webbrowser.open_new_tab('https://www.lipidmaps.org/databases/comp_db/download')
        elif db_name == 'LipidMaps_LMSD':
            webbrowser.open_new_tab('https://www.lipidmaps.org/databases/lmsd/download')
        elif db_name == 'METASPACE_Core_Metabolome_v3':
            webbrowser.open_new_tab('https://metaspace2020.eu/help')
        elif db_name == 'METASPACE_NGlycDB':
            webbrowser.open_new_tab('https://metaspace2020.eu/help')
        elif db_name == 'METLIN_SMRT':
            webbrowser.open_new_tab('https://figshare.com/articles/dataset/The_METLIN_small_molecule_dataset_for_machine_learning-based_retention_time_prediction/8038913')
        elif db_name == 'NPAtlas':
            webbrowser.open_new_tab('https://www.npatlas.org/download')
        elif db_name == 'Unified_CCS_Compendium':
            webbrowser.open_new_tab('https://github.com/McLeanResearchGroup/CCS-Compendium/tree/master/PCDL')

    source.bind("<Button-1>", open_source)

    window.mainloop()


if __name__ == '__main__':
    main()
