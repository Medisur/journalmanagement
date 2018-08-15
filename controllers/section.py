
def grid():

    query = db.issue

    if request.vars.journal_id:
        query = db.section.journal == int(request.vars.journal_id)
        db.section.journal.default = int(request.vars.journal_id)

    db.section.journal.readable = db.section.journal.writable = False

    grid = SQLFORM.grid(query, formname='section_grid',
                        # editable=auth.has_membership(GROUP_ADMIN),
                        # deletable=auth.has_membership(GROUP_ADMIN),
                        # create=auth.has_membership(GROUP_ADMIN),
                        details=False,
                        user_signature=True,
                        # args=[request.vars.journal_id]
                        )

    return dict(grid=grid)

