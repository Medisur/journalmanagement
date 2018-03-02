
def view():
    issue_id = request.args(0, cast=int) or redirect(URL('index'))
    issue = db(db.issue.id == issue_id).select().first()

    return dict(issue=issue)

def grid():

    query = db.issue

    if request.vars.journal_id:
        query = db.issue.journal == int(request.vars.journal_id)
        db.issue.journal.default = int(request.vars.journal_id)

    db.issue.journal.readable = db.issue.journal.writable = False

    grid = SQLFORM.grid(query, formname='issue_grid',
                        # editable=auth.has_membership(GROUP_ADMIN),
                        deletable=auth.has_membership(GROUP_ADMIN),
                        create=auth.has_membership(GROUP_ADMIN),
                        details=False,
                        links=[{'header': '', 'body': lambda row: A(T('View'), _href=URL('view', args=[row.id], extension=False))}],
                        user_signature=True,
                        # args=[journal_id]
                        )

    return dict(grid=grid)