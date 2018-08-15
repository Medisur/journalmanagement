
def grid():

    query = db.author

    if request.vars.article_id:
        query = db.author.article == int(request.vars.article_id)
        db.author.article.default = int(request.vars.article_id)

    db.author.article.readable = db.author.article.writable = False

    grid = SQLFORM.grid(query, formname='author_grid',
                        editable=auth.has_membership(GROUP_ADMIN),
                        deletable=auth.has_membership(GROUP_ADMIN),
                        create=auth.has_membership(GROUP_ADMIN),
                        details=False,
                        user_signature=True,
                        # args=[journal_id]
                        )

    return dict(grid=grid)