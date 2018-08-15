from gluon.serializers import json
import string
import random
from dateutil import parser

def _csl_object(row):
    citation_vars = {}
    citation = row.citation
    citation_parts = db(db.citation_part.citation == citation.id).select()
    for citation_part in citation_parts:
        citation_vars[citation_part.part] = citation_part.val
    citation_vars['id'] = citation.id
    return to_csl_object(citation_vars)

def _citation_parts(row):
    citation = row.citation
    rows = db(db.citation_part.citation == citation.id).select()

    parts = {}
    for row in rows:
        parts[row.part] = row.val

    return parts

def _add_citation_parts(row, parts):
    citation = row.citation
    for key in parts:
        if parts[key] and key[0] != "_" and key != 'id':
            validation_data = db.citation_part.validate_and_insert(
                citation=citation.id,
                part=key,
                val=parts[key]
            )
            if not validation_data.id:
                raise HTTP(503, validation_data)

def to_csl_object(vars):
    object = {}
    object['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    for key in vars:
        # remove custom form fields
        if not vars[key] or key[0] == "_":
            continue

        # names
        if key in ['author', 'collection-editor', 'composer', 'container-author', 'director', 'editor',
                   'editorial-director', 'interviewer', 'illustrator', 'original-author', 'recipient',
                   'reviewed-author', 'translator']:
            names = []
            if isinstance(vars[key], str):
                vars[key] = map(str.strip, vars[key].split(','))
            for name in vars[key]:
                name_obj = {}
                split_name = name.split(" ")
                name_obj['family'] = split_name[0]
                name_obj['given'] = " ".join(split_name[1:])
                names.append(name_obj)
            object[key]=names
            continue
        # dates
        if key in ['accessed', 'container', 'event-date', 'issued', 'original-date', 'submitted']:
            if vars[key]:
                d = parser.parse(vars[key])
                normalized_date = d.strftime("%d/%m/%Y")
                date = normalized_date.split("/")
                date_list = [date[2], date[1].lstrip('0'), date[0].lstrip('0')]
                object[key] = [{'date-parts':date_list}]
            continue
        #categories
        if key in ['categories']:
            categories = vars[key].split(",")
            map(str.strip, categories)
            object[key] = categories
            continue
        # if key in "issue":
        #     vars[key] = {"type":vars[key]}
        object[key]=str(vars[key])
    return object

def _on_citation_define(table):

    table.csl_object = Field.Virtual('csl_object', _csl_object)
    table.parts = Field.Virtual('parts', _citation_parts)
    table.add_parts = Field.Method(_add_citation_parts)

    table.article.requires = IS_IN_DB(db, db.article.id)


db.define_table('citation',
                Field('article', 'reference article'),
                Field('full_text', 'string', requires=IS_NOT_EMPTY(), label=T('Text')),
                on_define=_on_citation_define,
                )

