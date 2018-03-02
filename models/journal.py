
def _on_journal_define(table):
    pass


db.define_table('journal',
                Field('title', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Journal Title')),
                Field('subtitle', 'string', label=T('Journal Subtitle')),
                Field('short_title', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Journal Short Title')),
                Field('issn', 'string', label=T('ISSN')),
                Field('isbn', 'string', label=T('ISBN')),
                Field('publisher_name', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Publisher')),
                Field('publisher_location', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Publisher Location')),
                Field('publisher_id', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Publisher ID')),
                Field('email', 'string',
                      requires = IS_EMAIL(error_message=T('invalid email!')), label=T('Email')),
                Field('url', 'string',
                      requires = IS_URL(), label=T('URL')),
                Field('copyright', 'string', label=T('Copyright')),
                Field('copyright_year', 'string', label=T('Copyright Year')),
                Field('copyright_holder', 'string', label=T('Copyright Holder')),
                on_define=_on_journal_define,
                )