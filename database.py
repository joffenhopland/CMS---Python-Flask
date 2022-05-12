import mysql.connector


class db:
    def __init__(self) -> None:
        dbconfig = {'host': 'kark.uit.no',
                    'user': 'stud_v22_pedersenkri',
                    'password': 'pcQHe4vmK2Sc9JtS',
                    'database': 'stud_v22_pedersenkri', }
        self.configuration = dbconfig

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self

    def newUser(self, bruker):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            sql1 = '''INSERT INTO bruker (fornavn, etternavn, epost, passwordHash, verifiseringskode)
                VALUES (%s, %s, %s, %s, %s)'''
            cursor.execute(sql1, bruker)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def verifiser(self, kode):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id from bruker where verifiseringskode=(%s)", (kode,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

        if result == None:
            return False

        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            sql1 = '''UPDATE bruker
            SET verifisert = (%s) WHERE verifiseringskode = (%s)'''
            oppdater = (1, kode)
            cursor.execute(sql1, oppdater)
            conn.commit()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(err)

    def attemptedUser(self, epost):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT epost from bruker where epost=(%s)", (epost,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        if result == None:
            return False
        else:
            return result[0]

    def getUser(self, epost):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM bruker WHERE epost=(%s)", (epost,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result

    def getUser2(self, kode):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM bruker WHERE verifiseringskode=(%s)", (kode,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result

    def getPasswordHash(self, epost):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT passwordHash from bruker where epost=(%s)", (epost,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        if result == None:
            return False
        else:
            return result[0]

    def checkVerification(self, epost):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT verifisert from bruker where epost=(%s)", (epost,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        if result[0] == 0:
            return False
        else:
            return True

    def newDocument(self, dokument, folderId):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            sql1 = '''INSERT INTO dokument (
                tittel, beskrivelse, publisert, tilgang, fil, bruker_id, dokumentnavn, dokumenttype)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql1, dokument)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

        if folderId:
            try:
                doc_id = self.getdocid()
                conn = mysql.connector.connect(**self.configuration)
                cursor = conn.cursor()
                sql1 = '''UPDATE dokument
                SET katalog_ID = (%s) WHERE docId = (%s)'''
                input_data = (folderId, doc_id)
                cursor.execute(sql1, input_data)
                conn.commit()
                conn.close()
            except mysql.connector.Error as err:
                print(err)

    def newComment(self, kommentar):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            sql1 = '''INSERT INTO kommentar (
                tittel, publisert, tekst, dokument_docId, bruker_id)
                VALUES (%s, %s, %s, %s, %s)'''
            cursor.execute(sql1, kommentar)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def getComments(self, docId):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM kommentar WHERE dokument_docId=(%s)", (docId,))
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def getSpecificComment(self, comment_id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM kommentar WHERE id=(%s)", (comment_id,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result

    def deleteComment(self, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kommentar WHERE id = (%s)", (id,))
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def allDocuments(self):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM dokument")
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def getDocument(self, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM dokument WHERE docId=(%s)", (id,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result

    def getViews(self, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT visninger FROM dokument WHERE docId=(%s)", (id,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result[0]

    def updateViews(self, views, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            sql1 = '''UPDATE dokument
            SET visninger = (%s) WHERE docId = (%s)'''
            input_data = (views, id)
            cursor.execute(sql1, input_data)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def allTags(self):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tagname FROM tag")
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def tags(self):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tagId, tagname FROM tag")
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def newTag(self, tag):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            sql = '''INSERT INTO tag (
                tagname)
                VALUES (%s)'''
            insert = (tag,)
            cursor.execute(sql, insert)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def setDocTag(self, tag):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tagId FROM tag WHERE tagname=(%s)", (tag,))
            result = cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)

        tagId = result[0]
        docId = self.getdocid()

        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            sql = '''INSERT INTO doc_tag (
                tag_tagId, dokument_docId)
                VALUES (%s, %s)'''
            insert = (tagId, docId)
            cursor.execute(sql, insert)
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def deleteDocument(self, docId):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dokument WHERE docId = (%s)", (docId,))
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def updateDocument(self, tittel, beskrivelse, tilgang, docId):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE dokument SET tittel=(%s), beskrivelse=(%s), tilgang=(%s) WHERE docId=(%s)", (tittel, beskrivelse, tilgang, docId))
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)

    def getdocid(self):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT docId FROM dokument")
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)

        number = max(result)
        return number[0]

    def parentFolder(self, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            if id:
                cursor.execute(
                "SELECT id, kat_navn FROM Katalog where katalog_id is null")
            else:
                cursor.execute(
                "SELECT id, kat_navn FROM Katalog where katalog_id is null and tilgang = 0")
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def childFolder(self, parentId, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            if id:
                cursor.execute(
                    "SELECT id, kat_navn FROM Katalog where Katalog_id=(%s)", (parentId,))
            else:
                cursor.execute(
                    "SELECT id, kat_navn FROM Katalog where Katalog_id=(%s) and tilgang = 0", (parentId,))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def homepageDoc(self, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            if id:
                cursor.execute(
                    "SELECT * FROM dokument where Katalog_ID is null")
            else:
                cursor.execute(
                    "SELECT * FROM dokument where Katalog_ID is null and tilgang = 0")                
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def folderDocument(self, folderId, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            if id:
                cursor.execute(
                    "SELECT * FROM dokument where Katalog_ID=(%s)", (folderId,))
            else:
                cursor.execute(
                    "SELECT * FROM dokument where Katalog_ID=(%s) and tilgang = 0", (folderId,))                
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def newFolder(self, navn, tilgang, parent):
        try:
            if parent:
                conn = mysql.connector.connect(**self.configuration)
                cursor = conn.cursor()
                sql = '''INSERT INTO Katalog (
                    kat_navn, tilgang, Katalog_id)
                    VALUES (%s, %s, %s)'''
                new_folder = (navn, tilgang, parent)
                cursor.execute(sql, new_folder)
                conn.commit()
                conn.close()
            else:
                conn = mysql.connector.connect(**self.configuration)
                cursor = conn.cursor()
                sql = '''INSERT INTO Katalog (
                    kat_navn, tilgang)
                    VALUES (%s, %s)'''
                new_folder = (navn, tilgang)
                cursor.execute(sql, new_folder)
                conn.commit()
                conn.close()
        except mysql.connector.Error as err:
            print(err)


    def searchAll(self, search, userId):
        try:
            if userId:
                conn = mysql.connector.connect(**self.configuration)
                cursor = conn.cursor()
                cursor.execute(
                    "select * from dokument where publisert = (%s)  \
                    union \
                    select * from dokument where lower(tittel) like (%s) or lower(tittel) like (%s) \
                    union \
                    select * from dokument where lower(beskrivelse) like (%s) or lower(beskrivelse) like (%s)", (search, f'{search}%', f'%{search}', f'{search}%', f'%{search}'))
                result = cursor.fetchall()
                return result
            else:
                conn = mysql.connector.connect(**self.configuration)
                cursor = conn.cursor()
                cursor.execute(
                    "select * from dokument where publisert = (%s) and tilgang = 0 \
                    union \
                    select * from dokument where lower(tittel) like (%s) or lower(tittel) like (%s) and tilgang = 0 \
                    union \
                    select * from dokument where lower(beskrivelse) like (%s) or lower(beskrivelse) like (%s) and tilgang = 0", (search, f'{search}%', f'%{search}', f'{search}%', f'%{search}'))
                result = cursor.fetchall()
                return result
        except mysql.connector.Error as err:
            print(err)


    def searchDocTag(self, tagId, id):
        try:
            conn = mysql.connector.connect(**self.configuration)
            cursor = conn.cursor()
            if id:
                cursor.execute(
                "SELECT * FROM dokument, tag, doc_tag where dokument.docId = doc_tag.dokument_docId and doc_tag.tag_tagId = tag.tagId and tag.tagId =(%s)", (tagId,))
            else:
                                cursor.execute(
                "SELECT * FROM dokument, tag, doc_tag where dokument.docId = doc_tag.dokument_docId and doc_tag.tag_tagId = tag.tagId and dokument.tilgang = 0 and tag.tagId =(%s)", (tagId,))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)
