import os
import argparse
from rich.table import Table
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS, IFD
from pillow_heif import register_heif_opener
from rich.console import Console
from pathlib import Path
import shutil
import datetime
from rich.table import Table
from rich.panel import Panel

console = Console()

def parse_arguments():
    """Parses the command line arguments.
    the procesed flag is optional and defaults to False.
    Returns:
        A tuple containing the path to the directory to be searched and a boolean flag if the files are processed or not.
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", help="The path to the directory to be searched.", type=str, required=True)
        parser.add_argument("--destination", help="The path to the destination directory where the ordered images are stored.", type=str, default=".")
        parser.add_argument("--dry-run", action=argparse.BooleanOptionalAction, help="Dry run, do not copy files.", default=False)
        parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, help="Verbose output.", default=False)
        args = parser.parse_args()
        return args
    except:
        parser.print_help()
        exit(0)


def read_files(path: str):
    """
    Read files recursively in the given path. Retrieve the height and width of the image files using the imagesize library.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path
            

def get_lat_lon(exifdata):
    """
    Get the latitude and longitude from the exif data.
    """
    lat = None
    lon = None
    gps_ifd = exifdata.get_ifd(IFD.GPSInfo)
    if gps_ifd:
        gps_data = {}
        for tag, value in gps_ifd.items():
            decoded = GPSTAGS.get(tag, tag)
            gps_data[decoded] = value
        lat = gps_data.get('GPSLatitude')
        lon = gps_data.get('GPSLongitude')
    return lat, lon

def get_metadata(exifdata):
    """
    Get the metadata from the exif data.
    """
    month_name = None
    year = None
    month = None
    day = None
    model = None
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except:
                console.print(f'Error decoding data from {tag}', style="bold red")
        if tag == 'DateTime':
            year = data[:4]
            month = data[5:7]
            day = data[8:10]
            # check if valid datetime
            try:
                picture_taken = datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                console.print(f'Invalid date {year}-{month}-{day}. Set to 2000-01-01', style="bold red")
                picture_taken = datetime.datetime(2000, 1, 1)
                
            month_name =  picture_taken.strftime("%B")

        if tag == 'Model':
            # normalize model
            model = data.upper().replace(' ', '_')
    return year, month, day, month_name, model

if __name__ ==  "__main__":

    # Register the heif file format with Pillow
    register_heif_opener()
    
    # Parse the arguments from the command line
    parsed_args = parse_arguments()

    path = parsed_args.path
    dry_run = parsed_args.dry_run
    destination = parsed_args.destination
    verbose = parsed_args.verbose

    console.print(f'Reading files from {path}')
    if dry_run:
        console.print(Panel("Dry run, no files will be copied"))

    files = read_files(path)

    # count number of valid images and total size
    total_size_bytes = 0
    total_images = 0
    total_non_images = 0


    for f in files:

        file_size_in_bytes = os.path.getsize(f)
        total_size_bytes += file_size_in_bytes
        file_name = os.path.basename(f)
        if verbose:
            console.print(f'Processing {file_name} (size: {file_size_in_bytes} bytes)')
        target_path = os.path.join(destination, 'UNKNOWN')

        try:
            image = Image.open(f)
            exifdata = image.getexif()
            lat, lon = get_lat_lon(exifdata)
            year, month, day, month_name, model = get_metadata(exifdata)

            # check if all values are available
            if None in (year, month, day, month_name, model):
                console.print(f'No meta data extracted from {file_name}', style="bold red")
                total_non_images += 1
            else:
                total_images += 1
                target_path = os.path.join(destination, year, f'{month}_{month_name}', model)
        except:
            console.print(f'Error opening {file_name}. Seems to be no image file.', style="bold red")
            total_non_images += 1

        if dry_run:
            console.print(f'Copying {file_name} to {target_path}')
        else:
            if verbose:
                console.print(f'Creating folder {target_path} if it does not exist')

            # remove null bytes from target path
            target_path = target_path.replace('\x00', '')

            Path(target_path).mkdir(parents=True, exist_ok=True)
            # pass
            console.print(f'Copying {file_name} to ...{target_path}...', style="green bold")
            shutil.copy(f, f'{target_path}/{file_name}')

    total_size_in_megebytes = round(total_size_bytes / (1024 * 1024), 2)

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Total images", style="dim", width=15)
    table.add_column("Total non images", style="dim", width=15)
    table.add_column("Total size in Mb", style="dim", width=20)
    table.add_row(f'[green]{str(total_images)}[/green]', f'[red]{str(total_non_images)}[/red]', str(total_size_in_megebytes))
    console.print(table)