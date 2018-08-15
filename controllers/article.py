
def create():
    issue_id = request.args(0, cast=int) or redirect(URL('index'))
    db.article.issue.default = issue_id
    db.article.issue.readable = db.article.issue.writable = False

    form = SQLFORM(db.article)
    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('edit', args=[form.vars.id]))

    return dict(form=form)

def edit():
    article_id = request.args(0, cast=int) or redirect(URL('index'))
    article = db.article(article_id)
    db.article.id.readable = db.article.id.writable = False
    db.article.issue.readable = db.article.issue.writable = False
    form = SQLFORM(db.article, article_id)
    if form.process().accepted:
        response.flash = 'form accepted'

    return dict(form=form, article=article)

def grid():

    query = db.issue

    if request.vars.issue_id:
        query = db.article.issue == int(request.vars.issue_id)
        db.article.issue.default = int(request.vars.issue_id)

    db.article.issue.readable = db.article.issue.writable = False

    grid = SQLFORM.grid(query, formname='article_grid',
                        editable=False,
                        deletable=auth.has_membership(GROUP_ADMIN),
                        create=auth.has_membership(GROUP_ADMIN),
                        details=False,
                        links=[
                            # {
                            #     'header': '',
                            #     'body': lambda row: A(T('View'), _href=URL('view', args=[row.id]), extension=False)
                            # },
                            {
                                'header': '',
                                'body': lambda row: A(T('export'),
                                                      _href=URL('export_jats_xml', args=[row.id], extension=False))
                            },
                            {
                                'header': '',
                                'body': lambda row: A(T('Edit'), _href=URL('edit', args=[row.id], extension=False))
                            }
                        ],
                        user_signature=True,
                        # args=[journal_id]
                        )

    return dict(grid=grid)

def body():
    return dict(hello='hello')

def export_jats_xml():
    article_id = request.args(0, cast=int) or redirect(URL('index'))
    article = db.article(article_id)
    return article.get_jats_xml()