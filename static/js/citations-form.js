const Cite = require('citation-js');

$(function(){
    const citationsApiUrl = $("#citations-app").data("citationsApiUrl");
    const citationsFormat = $("#citations-app").data("citationsFormat");
    const articleId = $("#citations-app").data("articleId");

    var citationObjects = null;

    reloadCitations();

    function reloadCitations(){

        $('#citations-list').empty();

        loadCitations(articleId).then(function (objects) {
            citationObjects = objects;


            var csl_objects = [];
            citationObjects.map(function (citation) {
                csl_objects.push(citation.csl_object);
            });

            var citationOptions = {
                format: 'string',
                type: 'html',
                append: function (citation) {
                    return '<div class="citation-controls"><i class="fa fa-edit citation-edit"></i> <i class="fa fa-remove citation-remove"></i></div>';
                }
            };

            citations = assembleCitations(csl_objects, citationOptions);

            $('#citations-list').empty();
            $('#citations-list').append(citations);

        });

        $('#new-citation-button').click(function (a) {
            $('#citation-modal').modal("toggle");
        });
    }

    // includes formatUnicorn function for string formatting
    String.prototype.formatUnicorn = String.prototype.formatUnicorn ||
        function () {
            "use strict";
            var str = this.toString();
            if (arguments.length) {
                var t = typeof arguments[0];
                var key;
                var args = ("string" === t || "number" === t) ?
                    Array.prototype.slice.call(arguments)
                    : arguments[0];

                for (key in args) {
                    str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
                }
            }

            return str;
        };

    function assembleCitations(cslObject, options){
        // Assemble citations based on CSL object
        if (!options){
            options = {};
        }

        options.format = options.format ? options.format : 'string';
        options.type = options.type ? options.type : 'html';
        options.style = options.style ? options.style : 'citation-'+citationsFormat;
        options.lang = options.lang ? options.lang : 'es-ES';

        var newCite = new Cite(cslObject);

        return newCite.get(options);
    }

    function callCitationDataToCslJson(data) {
        // Calls data to csl_json service
        // Return: promise with csl object
        return $.getJSON(citationsApiUrl + '/to_csl_json/', data);
    }

    function toggleCitationModal(){
        $('#citation-modal').modal("toggle");
    }

    function loadCitations(articleId){

        return $.getJSON(citationsApiUrl+'/citations/' + articleId).then(function (data) {
            return data.data;
        });

    }

    function buildCitationFormPart(label, name, type, value){
        return $('<input>').attr({
            type: type,
            id: label+"_"+name,
            name: name,
            value: value
        });
    }

    function addCitationPart(label, name, type, value) {
        // Include a citation part in form if not exists

        if ($('#frmCitation input[name="'+name+'"]').length < 1){
            var str = '<div id="{name}_widget_container" class="form-group row"><label class="col-sm-3 col-form-label">{label}:</label><div class="col-sm-9">{content} <button class="btn" data-action="remove_citation_element" data-target="{name}">x</button><div></div>'.formatUnicorn({
                name: name,
                label: label,
                content: buildCitationFormPart(label, name, type, value).prop('outerHTML')
            });
            $('#citations-parts-container').append(str);
        }

    }

    function addCitationParts(parts){
        // include multiple parts to citation form
        parts.map(function (partName) {
            var label = $('#selectCitationPart option[value="'+partName+'"]').text();
            var type = getCitationPartType(partName);

            addCitationPart(label, partName, type, '');
        });
    }

    function removeCitationPart(name) {
        // Remove a citation form entry by name
        $("#"+name+"_widget_container").remove();
    }

    function cleanCitationsParts() {
        $('#citations-parts-container').empty();
        $('#citation-preview-container').empty();
    }

    function resetCitatonForm(){
        // Reset the citation form
        $('#selectCitationType').prop('selectedIndex',0);
        $('#selectCitationPart').prop('selectedIndex',0);
        $('#frmCitation input[name="type"]').val('');
        $('#frmCitation input[name="id"]').val('');
        $('#frmCitation input[name="_full_text"]').val('');
        cleanCitationsParts();
    }

    function newCitation(data) {
        // Post call to create a new citation using citation form data
        // Returns a Promise
        return $.ajax({
             type: "POST",
             url: citationsApiUrl+'/citation',
             data: data
        });
    }

    function updateCitation(id, data){
        // Put call to edit a citation using citation form data
        // Returns a Promise
        return $.ajax({
             type: "PUT",
             url: citationsApiUrl+'/citation/'+id,
             data: data
        });
    }

    function callDeleteCitation(citationId){
        // Delete call to remove a citation
        // Returns a Promise
        return $.ajax({
             type: "DELETE",
             url: citationsApiUrl+'/citation/'+citationId
        });
    }

    function getCitationPartType(name){
        var type = 'text';
        switch (name){
            case 'accessed' :
            case 'container' :
            case 'event-date' :
            case 'issued' :
            case 'original-date' :
            case 'submitted' :
                type = 'date';
                break;
            case 'URL':
                type = 'url';
                break;
        }
        return type;
    }

    function assembleFormCitation() {
        var citationData = $("#frmCitation").serialize();
        callCitationDataToCslJson(citationData)
            .then(function (data) {
                var newCitationHTML = assembleCitations(data.data);

                var newCitationStr = $.trim(assembleCitations(data.data, {type: 'string'})).slice(3);

                $('#citation-preview-container').empty();
                $('#citation-preview-container').append(newCitationHTML);
                $('#frmCitation input[name="_full_text"]').val(newCitationStr);
            });
    }

    function addCitationFormTemplate(name) {

        switch (name){
            case 'article-journal':
                addArticleTemplate();
                break;
            case 'book':
                addBookTemplate();
                break;
            case 'chapter':
                addChapterTemplate();
                break;
            case 'paper-conference':
                addPaperConferenceTemplate();
                break;
            case 'article-magazine':
                addArticleMagazineTemplate();
                break;
            case 'article-newspaper':
                addArticleNewspaperTemplate();
                break;
            case 'webpage':
                addWebpageTemplate();
                break;
        }
    }

    function addArticleTemplate() {
        // Includes journal-article parts to citation form
        var parts = [
            'title',
            'container-title',
            'author',
            'editor',
            'issue',
            'volume',
            'page',
            'URL',
            'DOI',
            'ISSN',
            'issued',
            'accessed'

        ];

        addCitationParts(parts);
    }

    function addBookTemplate() {
        // Includes Book parts to citation form
        var parts = [
            'title',
            'author',
            'editor',
            'edition',
            'volume',
            'publisher',
            'publisher-place',
            'URL',
            'ISBN',
            'issued',
            'accessed'
        ];

        addCitationParts(parts);
    }

    function addChapterTemplate() {
        // Includes Chapter parts to citation form
        var parts = [
            'title',
            'container-title',
            'author',
            'container-author',
            'editor',
            'edition',
            'volume',
            'page',
            'publisher',
            'publisher-place',
            'URL',
            'ISBN',
            'issued',
            'accessed'
        ];

        addCitationParts(parts);
    }

    function addPaperConferenceTemplate() {
        // Includes Paper Conference parts to citation form
        var parts = [
            'title',
            'author',
            'editor',
            'issue',
            'volume',
            'event',
            'publisher',
            'URL',
            'DOI',
            'ISBN',
            'issued',
            'accessed'
        ];

        addCitationParts(parts);
    }

    function addArticleMagazineTemplate() {
        // Includes Article Magazine parts to citation form
        var parts = [
            'title',
            'container-title',
            'author',
            'editor',
            'volume',
            'page',
            'URL',
            'ISSN',
            'issued',
            'accessed'
        ];

        addCitationParts(parts);
    }

    function addWebpageTemplate() {
        // Includes Webpage parts to citation form
        var parts = [
            'title',
            'container-title',
            'author',
            'URL',
            'issued',
            'accessed'
        ];

        addCitationParts(parts);
    }

    function addArticleNewspaperTemplate() {
        // Includes Article Newspaper parts to citation form
        var parts = [
            'title',
            'container-title',
            'author',
            'editor',
            'edition',
            'page',
            'publisher-place',
            'URL',
            'ISSN',
            'issued',
            'accessed'
        ];

        addCitationParts(parts);
    }

    // On citation Type changed
    $('#selectCitationType').change(function (e) {
        var value = $('#selectCitationType').val();
        $('#frmCitation input[name="type"]').val(value);

        addCitationFormTemplate(value);

    });

    // Click event for including a new citation part in form
    $('#btnAddCitationPart').click(function (e) {
        e.preventDefault();
        var label = $('#selectCitationPart option:selected').text();
        var name = $('#selectCitationPart').val();
        var type = getCitationPartType(name);

        addCitationPart(label, name, type, '');
    });

    // Remove citation part event
    $("#citations-parts-container").on("click","button[data-action='remove_citation_element']", function (e) {
        e.preventDefault();
        var name = $(this).data('target');
        removeCitationPart(name);
        assembleFormCitation();
    });

    // Form clear button event
    $('#btnFormClean').click(function (e) {
       resetCitatonForm();
    });

    // Citation modal close event
    $('#citation-modal').on('hidden.bs.modal', function (e) {
      resetCitatonForm();
    });

    // On citation form input change
    $("#frmCitation").on('change', 'input', function (e) {
        assembleFormCitation();
    });

    // Save citation event
    $('#btnFormReloadCitations').click(function (e) {
        e.preventDefault();
        var data = $("#frmCitation").serialize();

        var id = $("#frmCitation input[name='id']").val();

        if (!id) {
            // is a new citation, so we creates a new one
            newCitation(data)
                .then(function (data) {
                    $('#citation-modal').modal('hide');
                    reloadCitations();
                });
        } else {
            // we need to update a existent citation
            updateCitation(id, data)
                .then(function (data) {
                    $('#citation-modal').modal('hide');
                    reloadCitations();
                });
        }
    });

    // on click citation edit
    $("#citations-list").on("click",".citation-edit", function (e) {
        var entry = $(this).parent().parent();
        var citationId = entry.data("cslEntryId");

        var citation = citationObjects.find(function( obj ) { return obj.id == citationId; });


        var citationType = citation.parts.type;
        var citationId = citation.id;
        var citationFullText = citation.full_text;

        $('#frmCitation input[name="id"]').val(citationId);
        $('#frmCitation input[name="type"]').val(citationType);
        $('#frmCitation input[name="_full_text"]').val(citationFullText);


        $('#selectCitationType').val(citationType);

        for (partName in citation.parts){

            if ($.inArray(partName, ["type"]) >= 0){
                continue;
            }

            var label = $('#selectCitationPart option[value="'+partName+'"]').text();
            var partType = getCitationPartType(partName);
            var partValue = citation.parts[partName];

            addCitationPart(label, partName, partType, partValue);

        }

        assembleFormCitation();

        toggleCitationModal();

    });

    // on click citation delete
    $("#citations-list").on("click",".citation-remove", function (e) {
        var entry = $(this).parent().parent();
        var citationId = entry.data("cslEntryId");

        callDeleteCitation(citationId)
            .done(function () {
                reloadCitations();
            });

    });
});
