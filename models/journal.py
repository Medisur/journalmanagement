
def _on_journal_define(table):
    pass


db.define_table('journal',
                Field('title', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Journal Title')),
                Field('subtitle', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Journal Subtitle')),
                Field('short_title', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Journal Short Title')),
                Field('issn', 'string',
                      requires=IS_NOT_EMPTY(), label=T('ISSN')),
                Field('isbn', 'string',
                      requires=IS_NOT_EMPTY(), label=T('ISBN')),
                Field('publisher_name', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Publisher')),
                Field('publisher_location', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Publisher Location')),
                Field('email', 'string',
                      requires = IS_EMAIL(error_message=T('invalid email!')), label=T('Email')),
                Field('url', 'string',
                      requires = IS_URL(), label=T('URL')),
                on_define=_on_journal_define,
                )