# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----

def index():
    form=FORM(TABLE(TR(TD('Titulo del articulo'),TD(INPUT(_name='artic_tit',requires=IS_NOT_EMPTY()))),
                    TR(TD('Nombre de la revista'),TD(INPUT(_name='rev_tit',requires=IS_NOT_EMPTY()))),
                    TR(TD('Identificador de la revista'),TD(INPUT(_name='rev_id',requires=IS_NOT_EMPTY()))),
                    TR(TD('Abreviatura de la Rev.'),TD(INPUT(_name='rev_abb',requires=IS_NOT_EMPTY()))),
                    TR(TD('Organizacion de la Rev.'),TD(INPUT(_name='rev_org',requires=IS_NOT_EMPTY()))),
                    TR(TD('Localizacion de Organizacion'),TD(INPUT(_name='org_loc',requires=IS_NOT_EMPTY()))),
                    TR(TD('ISSN de la Rev.'),TD(INPUT(_name='rev_issn',requires=IS_NOT_EMPTY()))),
                    TR(TD(''),TD('')),
                    TR(TD('ID de Articulo'),TD(INPUT(_name='artic_id',requires=IS_NOT_EMPTY()))),
                    TR(TD('Categorias'),TD(INPUT(_name='artic_categ',requires=IS_NOT_EMPTY()))),
                    TR(TD(''),TD(INPUT(_type='submit')))))
    if form.accepts(request,session):
        redirect(URL('getxml',vars=dict(artic_tit=request.vars['artic_tit'],
                                        rev_tit=request.vars['rev_tit'],
                                        rev_id=request.vars['rev_id'],
                                        rev_abb=request.vars['rev_abb'],
                                        rev_org=request.vars['rev_org'],
                                        org_loc=request.vars['org_loc'],
                                        rev_issn=request.vars['rev_issn'],
                                        artic_id=request.vars['artic_id'],
                                        artic_categ=request.vars['artic_categ'],
                                       )))
    return dict(form=form)

def getxml():
    import lxml.builder as lb
    from lxml import etree
    from gluon.contrib.markdown.markdown2 import markdown
    #
    # Variables desde el formulario
    #
    variables=request.vars
    artic_tit=request.vars['artic_tit']
    rev_tit=request.vars['rev_tit'],
    rev_id=request.vars['rev_id']
    rev_abb=request.vars['rev_abb']
    rev_org=request.vars['rev_org']
    org_loc=request.vars['org_loc']
    rev_issn=request.vars['rev_issn']
    artic_id=request.vars['artic_id']
    artic_categ=request.vars['artic_categ'],
    #
    # Definicion del documento de salida como xml
    #
    response.headers['Content-Type']='application/xml'
    #
    #Espacio de nombres
    #
    nsmapp={'article-type':'research',
           'dtd-version':'1.1'}
    #
    #Etiquetas con hyphen
    #
    journalidmeta={'journal-id-type':'publisher-id'}
    articleidmeta={'pub-id-type':'publisher-id'}
    subjgrpcateg={'subj-group-type':'categories'}
    abbrtype={'abbrev-type':'publisher'}
    pubtype={'pub-type':'epub'}
    journalmeta=getattr(lb.E,'journal-meta')
    articlemeta=getattr(lb.E,'article-meta')
    articleid=getattr(lb.E,'article-id')
    articlecategories=getattr(lb.E,'article-categories')
    journalid=getattr(lb.E,'journal-id')
    journaltitlegrp=getattr(lb.E,'journal-title-group')
    journaltitle=getattr(lb.E,'journal-title')
    abbrjournaltitle=getattr(lb.E,'abbrev-journal-title')
    publishername=getattr(lb.E,'publisher-name')
    publisherloc=getattr(lb.E,'publisher-loc')
    subjgrp=getattr(lb.E,'subj-group')
    titlegrp=getattr(lb.E,'title-group')
    articletitle=getattr(lb.E,'article-title')
    #
    # Descomposicion de cadena de categorias para crear los elementos xml
    #
    categiterable=[]
    # de tupla a cadena
    cadenacategorias=str(artic_categ)
    cadenacategorias=cadenacategorias.replace("(","")
    cadenacategorias=cadenacategorias.replace(")","")
    listcategories=cadenacategorias.split(",")
    for item in listcategories:
        if item<>"":
                    categiterable.append(lb.E.subject("%s"%item))
    #
    #Insercion de espacio de nombres
    #
    E=lb.ElementMaker(nsmap={'xlink':'http://www.w3.org/1999/xlink'})
    #
    #Construccion del xml
    #
    documento= E.article(lb.E.front(journalmeta(journalid('%s'%rev_id,**journalidmeta),
                                                journaltitlegrp(journaltitle('%s'%rev_tit),
                                                                abbrjournaltitle('%s'%rev_abb,
                                                                **abbrtype)
                                                          ),
                                                lb.E.issn('%s'%rev_issn,**pubtype),
                                                lb.E.publisher(publishername('%s'%rev_org),
                                                         publisherloc('%s'%org_loc))
                                               ),
                                    articlemeta(articleid('%s'%artic_id,**articleidmeta),
                                               articlecategories(subjgrp(*categiterable,**subjgrpcateg)),
                                               titlegrp(articletitle('%s'%artic_tit)))
                        ),
                         **nsmapp)
    #
    #Publicacion del xml
    #
    return dict(T=XML(etree.tostring(documento,xml_declaration=True,encoding="ASCII",doctype='<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN" "http://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">',pretty_print=True)))



# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
