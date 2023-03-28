import peewee


# Create database
class BaseModel(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase('files.db')


class XML(BaseModel):
    class Meta:
        database = peewee.SqliteDatabase('files.db')

    Path = peewee.CharField(unique=True)
    File = peewee.TextField()
    Valid = peewee.BooleanField()
    Type = peewee.TextField(null=True)
    api = peewee.TextField(null=True)
    StatusCode = peewee.TextField(null=True)
    StatusText = peewee.TextField(null=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.Path

    def update_status(self, code, text):
        self.StatusCode = code
        self.StatusText = text
        self.save()
        pass


def CreateBase():
    try:
        XML.create_table()
        print("Table 'XML' created.")
    except peewee.OperationalError:
        print("Table 'XML' exists.")


def get_valid(qnt):
    return XML.select().limit(qnt).where(XML.Valid == 1 & XML.StatusCode.is_null() & XML.Type.is_null(False))


def has_something():
    return len(get_valid(1)) > 0


def count_valid():
    #return XML.select(peewee.fn.COUNT(XML.id)).where(XML.Valid == 1 & XML.StatusCode.is_null() & XML.Type.is_null(False) & XML.api != 'importarxmlcfearray').group_by(XML.StatusCode)
    return XML.select(peewee.fn.COUNT(XML.id)).where(
        XML.Valid == 1 & XML.StatusCode.is_null() & XML.Type.is_null(False)).group_by(
        XML.StatusCode
    )


def update_clean(status_for_cleaning):
    query = XML.update(StatusCode=None, StatusText=None).where(XML.StatusCode == status_for_cleaning)
    query.execute()
    print(f'Errors {status_for_cleaning} clear')
    pass


if __name__ == '__main__':
    CreateBase()
