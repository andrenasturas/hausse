from typing import Callable, List, Union, Optional

from hausse.lib import Plugin, Element
import logging
import csv
import sys


class CSVExpand(Plugin):
    """
        CSVExpand
        =========

        Loads CSV files as collections of elements.
    """

    def __init__(self, pattern = None, delimiter = ",", contents_column = None, filename_column = None):
        
        self.pattern = pattern
        self.delimiter = delimiter
        self.contents_column = contents_column
        self.filename_column = filename_column


    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        csv.field_size_limit(sys.maxsize)

        # Parsing elements
        for element in elements:

            # Valid selected CSV file
            if self.pattern and element._path.match(self.pattern) or self.pattern is None and element._path.suffix.lower() == ".csv":

                # Parsing CSV file
                records = csv.reader(element._contents.splitlines(), delimiter=self.delimiter)

                # Header line
                headers = next(records)

                # Iterating records
                for i, row in enumerate(records):

                    # Parsing CSV data into metadata
                    metadata = dict(zip(headers, row))

                    # Extracting main column contents
                    contents = metadata.pop(self.contents_column) if self.contents_column else None

                    # New filename building
                    filename = metadata.get(self.filename_column) if self.filename_column else str(i)
                    filepath = element._path.with_name(filename)
                    
                    new_file = Element(filepath, **metadata)
                    new_file._contents = contents

                    elements.append(new_file)

                # Removing original CSV file
                elements.remove(element)