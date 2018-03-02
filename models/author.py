
def _on_author_define(table):
    pass


db.define_table('author',
                Field('article', 'reference article'),
                Field('first_name', 'string',
                      requires=IS_NOT_EMPTY(), label=T('First Name')),
                Field('last_name', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Last Name')),
                Field('role', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Role')),

                Field('institution_name', 'string', label=T('Institution Name')),
                Field('institution_address', 'text', label=T('Institution Address')),
                Field('institution_city', 'string', label=T('Institution City')),
                Field('institution_state', 'string', label=T('Institution State')),
                Field('institution_country', 'string', label=T('Institution Country')),
                Field('institution_postal_code', 'string', label=T('Institution Postal Code')),
                Field('institution_phone', 'string', label=T('Institution Phone')),
                Field('institution_fax', 'string', label=T('Institution Fax')),
                Field('institution_email', 'string', label=T('Institution Email')),
                Field('institution_url', 'string', label=T('Institution URL')),

                on_define=_on_author_define,
                )