class BnpXmlWriter:
    def __init__(self, woid, flats, sheets, basename, structure):
        self.workOrderId = woid
        self.numberOfFlats = flats
        self.numberOfSheets = sheets
        self.bottomInBaseName = basename
        self.structure = structure
