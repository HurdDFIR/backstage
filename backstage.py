import csv 
from pathlib import Path
import argparse
from rich import print as rprint
from glob import glob
from backstage_record import Record
from colorama import Fore, Back, Style
import logging
from rich.logging import RichHandler
from rich.progress import Progress
from rich.traceback import install


def main():
    __author__ = "Stephen Hurd"
    __moniker__ = 'HurdDFIR'
    __version__ = "1.0.0"
    __description__ = "Microsoft Backstage Parser. This will parse Microsoft Backstage files into a CSV file."
    parser = argparse.ArgumentParser()
    parser.description = __description__
    parser.epilog = f'{__author__} | {__moniker__} | v:{__version__}'
    parser.add_argument('--drive', '-d', required=True, type=Path, help='Drive to search. Eg: C:\\')
    parser.add_argument('--output', '-o', required=True, type=Path, help='Output path. Eg: C:\\output.csv')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    FORMAT = "%(message)s"
    if args.verbose:
        logging.basicConfig(level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])
        install(show_locals=True, word_wrap=True)
    else:
        logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])
        install(word_wrap=True)


    log = logging.getLogger()
    


    print(f"""{Fore.MAGENTA}\
__________    _____  _________  ____  __.  _________________________    ___________________
\______   \  /  _  \ \_   ___ \|    |/ _| /   _____/\__    ___/  _  \  /  _____/\_   _____/
 |    |  _/ /  /_\  \/    \  \/|      <   \_____  \   |    | /  /_\  \/   \  ___ |    __)_ 
 |    |   \/    |    \     \___|    |  \  /        \  |    |/    |    \    \_\  \|        \\
 |______  /\____|__  /\______  /____|__ \/_______  /  |____|\____|__  /\______  /_______  /
        \/         \/        \/        \/        \/        {Fore.RESET}@{__moniker__}{Fore.MAGENTA}\/  {Fore.RESET}v{__version__}{Fore.MAGENTA}\/        \/
--------------------------------------------------------------------------------------------{Fore.RESET}""")
    log.debug("Starting Backstage Parser...")
    output = args.output
    drive = args.drive

    if not drive.exists():
        log.error(f'{drive} drive does not exist')
        exit(1)

    log.debug(f'Output path: {output}')
    files = glob(f'{drive}users\\*\\AppData\\Local\\Microsoft\\Office\\16.0\\BackstageInAppNavCache\\**\\*.json', recursive=True)
    log.debug(f'Found {len(files)} files')
    if len(files) == 0:
        log.error('No files found')
        exit(1)


    data = []

    with Progress() as progress:
        task = progress.add_task("Parsing...", total=len(files))

        for file in files:
            log.debug(file)
            d = Record(file).parse()
            data += d 
            progress.update(task, advance=1)
        
        task2 = progress.add_task("Sorting fieldnames...", total=len(data))
        fieldnames = []
        for d in data:
            for k in d.keys():
                if k not in fieldnames:
                    fieldnames.append(k)
            progress.update(task2, advance=1)
        
        task3 = progress.add_task(f"Writing {output}", total=len(data))
        with open(output, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
                progress.update(task3, advance=1)

if __name__ == "__main__":
    main()