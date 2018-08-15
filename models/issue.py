
def _on_issue_define(table):
    pass


db.define_table('issue',
                Field('journal', 'reference journal'),
                Field('volume', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Volume')),
                Field('issue', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Issue')),
                Field('publication_date', 'date', label=T('Publication Date')),
                on_define=_on_issue_define,
                )