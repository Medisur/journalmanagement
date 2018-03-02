
# def index():
#     grid = SQLFORM.grid(db.journal,
#                         # editable=auth.has_membership(GROUP_ADMIN),
#                         deletable=auth.has_membership(GROUP_ADMIN),
#                         create=auth.has_membership(GROUP_ADMIN),
#                         details=False,
#                         links=[{'header': '', 'body':lambda row: A(T('View'), _href=URL('view', args=[row.id]))}],
#                         user_signature=True)
#     return dict(grid=grid)

def grid():
    grid = SQLFORM.grid(db.journal,
                        # editable=auth.has_membership(GROUP_ADMIN),
                        deletable=auth.has_membership(GROUP_ADMIN),
                        create=auth.has_membership(GROUP_ADMIN),
                        details=False,
                        links=[{'header': '', 'body':lambda row: A(T('View'), _href=URL('view', args=[row.id], extension=False))}],
                        user_signature=True)
    return dict(grid=grid)


def view():
    journal_id = request.args(0, cast=int) or redirect(URL('index'))
    journal = db(db.journal.id == journal_id).select().first()

    # db.issue.journal.default = journal_id
    #
    # db.issue.journal.readable = db.issue.journal.writable = False

    # grid = SQLFORM.grid(db.issue.journal == journal.id,
    #                     # editable=auth.has_membership(GROUP_ADMIN),
    #                     deletable=auth.has_membership(GROUP_ADMIN),
    #                     create=auth.has_membership(GROUP_ADMIN),
    #                     details=False,
    #                     links=[{'header': '', 'body':lambda row: A(T('View'), _href=URL('view', args=[row.id]))}],
    #                     user_signature=True,
    #                     args=[journal_id])
    # # grid = SQLFORM.grid(db.issue)

    return dict(journal=journal)