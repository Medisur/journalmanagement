
def _on_citation_part_define(table):
    pass


db.define_table('citation_part',
                Field('citation', 'reference citation'),
                Field('part', 'string', requires=IS_NOT_EMPTY(), label=T('Name')),
                Field('val', 'string', requires=IS_NOT_EMPTY(), label=T('Value')),
                on_define=_on_citation_part_define,
                )

