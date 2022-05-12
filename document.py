class Document():

    # construct document object to use for pre populating form fields on edit page
    def __init__(self, docId, tittel, beskrivelse, publisert, tilgang, fil, bruker_id, visninger, Katalog_ID, dokumentnavn, dokumenttype):
        self.docId = docId
        self.tittel = tittel
        self.beskrivelse = beskrivelse
        self.publisert = publisert
        self.tilgang = tilgang
        self.fil = fil
        self.bruker_id = bruker_id
        self.visninger = visninger
        self.Katalog_ID = Katalog_ID
        self.dokumentnavn = dokumentnavn
        self.dokumenttype = dokumenttype
