# -*- coding: utf-8 -*-
from applications.journalmanagement.modules.api_utils import json_response

CITATIONS_API_NAME = "Citations"

def index():
    return dict(message="hello from citation.py")

def article_citations():
    # article_id = request.vars('article_id', cast=int) or redirect(URL('index'))
    article_id = request.vars['article_id'] or redirect(URL('index'))
    return dict(article_id=article_id)

def new():

    # import json
    # from citeproc import CitationStylesStyle, CitationStylesBibliography
    # from citeproc import Citation, CitationItem
    # from citeproc import formatter
    # from citeproc.source.json import CiteProcJSON
    #
    # citations = db(db.citation).select()
    # for citation in citations:
    #     print(citation)
    #     bib_source = CiteProcJSON([citation.csl_object])
    #     bib_style = CitationStylesStyle('/home/carlos.caballero/www/elsevier-vancouver.csl', validate=False)
    #     bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.plain)
    #     citation1 = Citation([CitationItem('17')])
    #     bibliography.register(citation1)
    #     def warn(citation_item):
    #         print("WARNING: Reference with key '{}' not found in the bibliography."
    #             .format(citation_item.key))
    #     print(bibliography.cite(citation1, warn))
    #     for item in bibliography.bibliography():
    #         print(str(item))


    form = SQLFORM.factory(
        Field('your_name', requires=IS_NOT_EMPTY()),
        Field('your_image', 'datetime'))
    if form.process().accepted:
        response.flash = 'form accepted'
        session.your_name = form.vars.your_name
        session.your_image = form.vars.your_image
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)



@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):

        if args[0] == 'citations' and args[1]:
            citations = db(db.citation.article == int(args[1])).select(db.citation.ALL)
            return json_response(CITATIONS_API_NAME, citations)

        if args[0] == 'to_csl_json':
            return json_response(CITATIONS_API_NAME, to_csl_object(vars))

        return dict()

    def POST(*args, **vars):

        if args[0] == 'citation':
            validation_data = db.citation.validate_and_insert(article=vars['article'], full_text=vars['_full_text'])
            if not validation_data.id:
                return json_response(CITATIONS_API_NAME, validation_data, 503)
            new_citation_id = validation_data.id
            citation = db(db.citation.id == validation_data.id).select().first()
            try:
                citation.add_parts(vars)
            except HTTP as e:
                return json_response(CITATIONS_API_NAME, e.body, 503)
                # raise HTTP(503, json(e.body))

            return json_response(CITATIONS_API_NAME, db(db.citation.id == new_citation_id).select())
            # return dict(data=db(db.citation.id == new_citation_id).select())

        return dict()

    def PUT(*args, **vars):
        if args[0] == 'citation':
            validation_data = db(db.citation.id == args[1]).validate_and_update(full_text=vars['_full_text'])
            if validation_data.errors:
                # raise HTTP(503, json(validation_data))
                return json_response(CITATIONS_API_NAME, validation_data, 503)
            elif validation_data.updated == 0:
                return json_response(CITATIONS_API_NAME, "Not found", 404)
            citation_id = args[1]
            if not db(db.citation_part.citation == citation_id).delete():
                return json_response(CITATIONS_API_NAME, "Can't delete", 503)
                # raise HTTP(503)
            citation = db(db.citation.id == citation_id).select().first()
            try:
                citation.add_parts(vars)
            except HTTP as e:
                return json_response(CITATIONS_API_NAME, e.body, 503)

            # return dict(data=citation)
            return json_response(CITATIONS_API_NAME, citation)


        return dict()

    def DELETE(*args, **vars):
        if args[0] == 'citation':
            if not db(db.citation.id == args[1]).delete():
                raise HTTP(503)
        return dict()

    return locals()


# from gluon.storage import Storage
# def form_tool():
#     response.generic_patterns.append('.json')
#     """
#     Return a form field html string (pretty ugly but handily)
#
#     """
#     tablename = request.args[0]
#     name = request.args[1]
#     type = request.args[2]
#
#     try:
#         value = request.args[3]
#     except:
#         value = ''
#
#     args = request.vars if request.vars else {}
#
#     field = Storage(dict(tablename=tablename, name=name, type=type))
#     return dict(content=SQLFORM.widgets[type].widget(field, value, **args))