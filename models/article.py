import xml.etree.ElementTree as xml

from io import StringIO
from io import BytesIO

from gluon.contenttype import contenttype

def _get_journal(row):
    article = row.article
    return db(
        (db.article.id == article.id) &
        (db.article.issue == db.issue.id) &
        (db.journal.id == db.issue.journal)
    ).select(db.journal.ALL).first()

def _get_issue(row):
    article = row.article
    return db(
        (db.article.id == article.id) &
        (db.article.issue == db.issue.id)
    ).select(db.issue.ALL).first()

def _get_authors(row):
    article = row.article
    return db(
        (db.author.article == article.id)
    ).select(db.author.ALL)


def _get_as_jats_xml(row):
    """
    Return an article as a JATS-XML
    TODO: refactor ths function (maybe move code to a module)
    """
    article = row.article

    journal = article.get_journal()
    issue = article.get_issue()
    authors = article.get_authors()

    article_element = xml.Element(
        "article",
        attrib={
            'article-type':"research-article",
            'dtd-version': '1.1d1',
            'xml:lang': 'en'
        }
    )

    # Article Front
    front_element = xml.SubElement(article_element, "front")

    journal_meta_element = xml.SubElement(front_element, "journal-meta")

    # Journal ID
    journal_id_publisher_element = xml.SubElement(journal_meta_element, "journal-id",
        attrib={
            'journal-id-type': 'publisher-id'
        }
    )
    journal_id_publisher_element.text = journal.publisher_id

    journal_id_element = xml.SubElement(journal_meta_element, "journal-id", attrib={
        'journal-id-type': 'nlm-ta'
    })
    journal_id_element.text = journal.title

    # Journal ISSN
    if journal.issn:
        journal_issn_element = xml.SubElement(journal_meta_element, 'issn')
        journal_issn_element.text = journal.issn

    # Journal ISBN
    if journal.isbn:
        journal_isbn_element = xml.SubElement(journal_meta_element, 'isbn')
        journal_isbn_element.text = journal.isbn

    # Journal Publisher
    journal_publisher_element = xml.SubElement(journal_meta_element, 'publisher')
    journal_publisher_name_element = xml.SubElement(journal_publisher_element, 'publisher-name')
    journal_publisher_name_element.text = journal.publisher_name


    article_meta_element = xml.SubElement(front_element, "article-meta")

    # Article ID
    article_id_element = xml.SubElement(article_meta_element, "article-id", attrib={
        'pub-id-type': 'other'
    })
    article_id_element.text = str(article.id)

    # Article Categories
    article_categories_element = xml.SubElement(article_meta_element, "article-categories")
    article_subj_group_element = xml.SubElement(article_categories_element, "subj-group", attrib={
        'subj-group-type': 'heading'
    })
    article_subj_group_subject_element = xml.SubElement(article_subj_group_element, "subject")
    article_subj_group_subject_element.text = article.section.title

    # Article Title Group
    article_title_group_element = xml.SubElement(article_meta_element, 'title-group')
    article_title_element = xml.SubElement(article_title_group_element, 'article-title')
    article_title_element.text = article.title
    if article.subtitle:
        article_subtitle_element = xml.SubElement(article_title_group_element, 'subtitle')
        article_subtitle_element.text = article.subtitle

    # Article Authors
    if authors:
        article_contrib_group_element = xml.SubElement(article_meta_element, 'contrib-group')
        author_counter = 0
        for author in authors:
            author_counter += 1
            author_aff_id = 'aff-{0}'.format(author_counter)

            article_contrib_element = xml.SubElement(article_contrib_group_element, 'contrib', attrib={
                'contrib-type': 'author'
            })
            article_author_name_element = xml.SubElement(article_contrib_element, 'name')
            article_author_surname_element = xml.SubElement(article_author_name_element, 'surname')
            article_author_surname_element.text = author.first_name
            article_author_givennames_element = xml.SubElement(article_author_name_element, 'given-names')
            article_author_givennames_element.text = author.last_name

            if author.role:
                article_author_role_element = xml.SubElement(article_contrib_element, 'role')
                article_author_role_element.text = author.role

            if author.institution_name:
                article_author_aff_element = xml.SubElement(article_contrib_element, 'aff')
                article_author_aff_element.text = author.institution_name

            if author.institution_address:
                article_author_aff_element.text +=  ", "+author.institution_address

                article_author_address_element = xml.SubElement(article_contrib_element, 'address')

                if author.institution_name:
                    article_author_institution_element = xml.SubElement(article_author_address_element, 'institution')
                    article_author_institution_element.text = author.institution_name

                if author.institution_address:
                    article_author_addrline_element = xml.SubElement(article_author_address_element, 'addr-line')
                    article_author_addrline_element.text = author.institution_address

                if author.institution_city:
                    article_author_city_element = xml.SubElement(article_author_address_element, 'city')
                    article_author_city_element.text = author.institution_city

                if author.institution_state:
                    article_author_state_element = xml.SubElement(article_author_address_element, 'state')
                    article_author_state_element.text = author.institution_state

                if author.institution_country:
                    article_author_country_element = xml.SubElement(article_author_address_element, 'country')
                    article_author_country_element.text = author.institution_country

                if author.institution_postal_code:
                    article_author_zipcode_element = xml.SubElement(article_author_address_element, 'postal-code')
                    article_author_zipcode_element.text = author.institution_postal_code

                if author.institution_phone:
                    article_author_phone_element = xml.SubElement(article_author_address_element, 'phone')
                    article_author_phone_element.text = author.institution_phone

                if author.institution_fax:
                    article_author_fax_element = xml.SubElement(article_author_address_element, 'fax')
                    article_author_fax_element.text = author.institution_fax

                if author.institution_email:
                    article_author_email_element = xml.SubElement(article_author_address_element, 'email')
                    article_author_email_element.text = author.institution_email

                if author.institution_url:
                    article_author_url_element = xml.SubElement(article_author_address_element, 'uri')
                    article_author_url_element.text = author.institution_url

            # article_author_xref_element = xml.SubElement(article_contrib_element, 'xref', attrib={
            #     'ref-type': 'aff',
            #     'rid': author_aff_id
            # })
            # article_aff_element = xml.SubElement(article_contrib_group_element, 'aff', attrib={
            #     'id': 'author_aff_id'
            # })
            # article_aff_element.text = author.institution_name

    # Article Publication Date
    if article.pub_date:
        article_pubdate_element = xml.SubElement(article_meta_element, 'pub-date', attrib={
            'date-type': 'pub',
            # TODO: include "print" publication format
            'publication-format': 'electronic',
            'iso-8601-date': article.pub_date.isoformat()
        })
        article_day_element = xml.SubElement(article_pubdate_element, 'day')
        article_day_element.text = str(article.pub_date.day)
        article_month_element = xml.SubElement(article_pubdate_element, 'month')
        article_month_element.text = str(article.pub_date.month)
        article_year_element = xml.SubElement(article_pubdate_element, 'year')
        article_year_element.text = str(article.pub_date.year)

    # Article Volume
    article_volume_element = xml.SubElement(article_meta_element, 'volume')
    article_volume_element.text = issue.volume

    # Article Issue
    article_issue_element = xml.SubElement(article_meta_element, 'issue')
    article_issue_element.text = issue.issue

    # Article Pages
    if article.first_page:
        article_fpage_element = xml.SubElement(article_meta_element, 'fpage')
        article_fpage_element.text = str(article.first_page)

    if article.last_page:
        article_lpage_element = xml.SubElement(article_meta_element, 'lpage')
        article_lpage_element.text = str(article.last_page)

    # Article History
    # TODO: add received date
    if article.accepted_date:
        article_history_element = xml.SubElement(article_meta_element, 'history')
        article_accepted_element = xml.SubElement(article_history_element, 'date', attrib={
            'date-type': 'accepted',
            'iso-8601-date': article.accepted_date.isoformat()
        })
        article_accepted_day_element = xml.SubElement(article_accepted_element, 'day')
        article_accepted_day_element.text = str(article.accepted_date.day)
        article_accepted_month_element = xml.SubElement(article_accepted_element, 'month')
        article_accepted_month_element.text = str(article.accepted_date.month)
        article_accepted_year_element = xml.SubElement(article_accepted_element, 'year')
        article_accepted_year_element.text = str(article.accepted_date.year)

    # Article Copyright
    if journal.copyright:
        article_permission_element = xml.SubElement(article_meta_element, 'permission')
        article_copyright_element = xml.SubElement(article_permission_element, 'copyright')
        article_copyright_element.text = journal.copyright
        if journal.copyright_year:
            article_copyright_year_element = xml.SubElement(article_permission_element, 'copyright-year')
            article_copyright_year_element.text = str(journal.copyright_year)
        if journal.copyright_holder:
            article_copyright_holder_element = xml.SubElement(article_permission_element, 'copyright-holder')
            article_copyright_holder_element.text = str(journal.copyright_holder)


    buffer = BytesIO()
    buffer.write('<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1d1 20130915//EN" "JATS-journalpublishing1.dtd">'.encode())
    xml.ElementTree(article_element).write(buffer, 'utf-8')

    response.headers['Content-Type'] = contenttype('.xml')
    return buffer.getvalue()

def _on_article_define(table):
    table.get_jats_xml = Field.Method('get_jats_xml', _get_as_jats_xml)
    table.get_journal = Field.Method('get_journal', _get_journal)
    table.get_issue = Field.Method('get_issue', _get_issue)
    table.get_authors = Field.Method('get_authors', _get_authors)
    pass


db.define_table('article',
                Field('issue', 'reference issue'),
                Field('title', 'string',
                      requires=IS_NOT_EMPTY(), label=T('Article Title')),
                Field('subtitle', 'string', label=T('Article Subtitle')),
                Field('first_page', 'integer', label=T('First Page')),
                Field('last_page', 'integer', label=T('Last Page')),
                Field('section', 'reference section'),
                Field('pub_date', 'date', label=T('Publication Date')),
                Field('accepted_date', 'date', label=T('Accepted')),
                on_define=_on_article_define,
                )



