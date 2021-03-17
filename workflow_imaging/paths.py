import datajoint as dj
import pathlib


def get_imaging_root_data_dir():
    data_dir = dj.config.get('custom', {}).get('imaging_root_data_dir', None)
    return pathlib.Path(data_dir) if data_dir else None


def get_scan_image_files(scan_key):
    # Folder structure: root / subject / session / .tif (raw)
    data_dir = get_imaging_root_data_dir()

    from .pipeline import Session
    sess_dir = data_dir / (Session.Directory & scan_key).fetch1('session_dir')

    if not sess_dir.exists():
        raise FileNotFoundError(f'Session directory not found ({sess_dir})')

    tiff_filepaths = [fp.as_posix() for fp in sess_dir.glob('*.tif')]
    if tiff_filepaths:
        return tiff_filepaths
    else:
        raise FileNotFoundError(f'No tiff file found in {sess_dir}')


def get_scan_box_files(scan_key):
    # Folder structure: root / subject / session / .sbx
    data_dir = get_imaging_root_data_dir()

    from .pipeline import Session
    sess_dir = data_dir / (Session.Directory & scan_key).fetch1('session_dir')

    if not sess_dir.exists():
        raise FileNotFoundError(f'Session directory not found ({sess_dir})')

    sbx_filepaths = [fp.as_posix() for fp in sess_dir.glob('*.sbx')]
    if sbx_filepaths:
        return sbx_filepaths
    else:
        raise FileNotFoundError(f'No .sbx file found in {sess_dir}')
