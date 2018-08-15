
def _on_section_define(table):
    pass


db.define_table('section',
                Field('title', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Section Title')),
                Field('journal', 'reference journal'),
                on_define=_on_section_define,
                format='%(title)s'
                )