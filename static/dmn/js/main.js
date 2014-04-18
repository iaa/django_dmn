$(document).ready(function(){
    /*  Alert Message
    ================================================== */
    $(".ifadein").fadeIn();
    //$(".ifadeout").delay(5000).fadeOut();
    $('.ttip').tooltip();
    $('.input_auto').popover();

    $(".table tbody tr").hover(
        function() { $(this).children('td').children('.operation').children('.btn-group').css('display', 'block');},
        function() { $(this).children('td').children('.operation').children('.btn-group').css('display', 'none');}
    );
    $(".toggle_field_search").toggle(
        function() { $('.field_search').fadeIn();},
        function() { $('.field_search').fadeOut();}
    );
    $(".toggle_field_hidden").toggle(
        function() { $('.field_hidden').fadeIn();},
        function() { $('.field_hidden').fadeOut();}
    );
    $(".itoggle").toggle(
        function() { $('.itoggle_div').fadeIn();},
        function() { $('.itoggle_div').fadeOut();}
    );
    /*$("td.header").hover(
        function() { $(this).addClass('bgray');},
        function() { $(this).removeClass('bgray');}
    );*/
    /*  Sort by grig with cookies
    ================================================== */
    // var cgsort_by = '';
    
    // if ($.cookie('j_grid_sort_by')) {
    //     cgsort_by = $.cookie('j_grid_sort_by');
    // };
    // if ($.cookie('j_grid_sort')) {
    //     cgsort = $.cookie('j_grid_sort');
    // };
    // if ( $.cookie('j_grid_sort_by') === 'ASC' ) {
    //         $(".j_grid_sort#"+cgsort).addClass('sorting_desc');         
    // };
    // if ( cgsort_by === 'DESC' ) {
    //         $(".j_grid_sort#"+cgsort).addClass('sorting_asc');         
    // };

    // $(".j_grid_sort").click(function() {
    //         $(".j_grid_sort").removeClass('sorting_asc');
    //         $(".j_grid_sort").removeClass('sorting_desc');
    //         $.cookie('j_grid_sort', $(this).attr('id'));
    //         if (!cgsort_by) $.cookie('j_grid_sort_by', 'DESC');
    //             if ( cgsort_by === 'ASC' ) {
    //                 $.cookie('j_grid_sort_by', 'DESC');
    //                 $(this).removeClass('sorting_desc');
    //                 $(this).addClass('sorting_asc');
    //             };
    //             if ( cgsort_by === 'DESC' ) {
    //                 $.cookie('j_grid_sort_by', 'ASC');
    //                 $(this).removeClass('sorting_asc');
    //                 $(this).addClass('sorting_desc');
    //             };
    //     window.location.reload(true);
            
    // });

    // $(".j_field_hidden_button").click(function() {
    //         // $.cookie.json = true;
    //         var name = $(this).attr('name');
    //         var model = $(this).attr('model');
    //         var cook_name = 'field_hidden_'+model
    //         var arr = []
    //         if ($.cookie(cook_name)) {
    //             arr = $.cookie(cook_name).split(',');
    //             if($.inArray(name,arr) == -1){
    //                 arr.push(name);
    //             }
    //             $.cookie(cook_name, arr.join(','));
    //         }
    //         else {
    //             arr.push(name);
    //             $.cookie(cook_name, arr);
    //         }
    //         window.location.reload(true);
    // });

    // $(".j_field_show_button").live("click", function() {
    //         // $.cookie.json = true;
    //         var name = $(this).attr('name');
    //         var model = $(this).attr('model');
    //         var cook_name = 'field_hidden_'+model;
    //         var arr = []
    //         arr = $.cookie(cook_name).split(',');
    //         $.each(arr, function(k, v) {
    //             if (name == v) {
    //                 arr.splice(k, 1)
    //             }
    //         });
    //         $.cookie(cook_name, arr.join(','));
    //         window.location.reload(true);
    // });

    /* Many checkboxes for grid DELETE
    ================================================== */

    $("#chbx_global").click( function(){
       if ($("#chbx_global").attr('checked')) {
            $('.chbx').attr('checked', true);
            $('.chbx_delete').fadeIn()
        }else{
            $('.chbx').attr('checked', false);
            $('.chbx_delete').fadeOut()
        }
    });

    $(".chbx").click( function(){
       if ($('.chbx').filter(':checked').size() > 0) {
            $('.chbx_delete').fadeIn()
        }
        else {
            $('.chbx_delete').fadeOut()
        }
    });

    $(".chbx_delete").click( function(){
        var chbx_id = [];
        var model = $(this).attr('name');
        $('.chbx').filter(':checked').each(function(){
           chbx_id.push(this.value); 
        });
        if (chbx_id.length !=0) {
          if (confirm("Удалить выбранное безвозвратно?")) {
            window.location.href='/dmn/'+model+'/destroymore/?destroy_arr='+chbx_id;
            //alert('/idmn/dmn/'+model+'/destroy/?destroy_arr='+chbx_id);
          };  
        };
    });

    $('.confirm_delete').live("click", function(){
        var model = $(this).attr('name');
        var id = $(this).attr('id');
        if (confirm("Удалить выбранное безвозвратно?")) {
            //window.location.href='/dmn/'+model+'/destroy/'+id;
            //$.post('/dmn/'+model+'/destroy/'+id);
            $.post( '/dmn/'+model+'/destroy/'+id, { 'id' : id }, function() {
                window.location.href = '/dmn/'+model+'/destroy/'+id;
            });
        }
        else {
            return false;
        }
    });

    /* Checkboxes for TOGGLE
    ================================================== */

    $(".chbx_toggle").click( function(){
        var model = $(this).attr('model');
        var id = $(this).attr('id');
        var attr = $(this).attr('name');
        window.location.href='/dmn/'+model+'/toggle/'+attr+'/'+id
    });

     /* TreeView
    ================================================== */

    $(".tree_icon").hover( 
        function(){
            $(this).addClass('hover');
        },
        function(){
            $(this).removeClass('hover');
        }
    );

    $('.tree_icon').tooltip();
    $('.itwipsy').tooltip();

    /*$('body').on('click','.tree_destroy',function()
        {return confirm('Удалить без возможности восстановления?');});*/
    
    $(".tree_icon").click( 
        function(){

            var model = $(this).siblings('.model').attr('name');
            var attr = $(this).attr('name');

            if ( $(this).hasClass('tree_update') ) {
                window.location.href='/dmn/'+model+'/update/'+attr;
            }
            if ( $(this).hasClass('tree_create') ) {
                window.location.href='/dmn/'+model+'/create/'+attr;
            }
            if ( $(this).hasClass('tree_hide') ) {
                window.location.href='/dmn/'+model+'/toggle/attr/deleted/id/'+attr;
            }
            /*if ( $(this).hasClass('tree_destroy') ) {
                window.location.href='/dmn/'+model+'/destroy/'+attr;
            }*/

        }
    );

     $(".getwell").click(
            function(){
                $('.showwell').fadeOut(0);
                $(this).siblings('.showwell').fadeIn();
            }
    );

    $(".close").click( function(){
       $(this).parent('.showwell').fadeOut();
    });

    /* GridDblclick
    ================================================== */
    $('.dblcl').dblclick(function() {

        if($(this).has("div").length) {

            var text1 = $('form').find('.form').text();
            $('table').find('.toform').html(text1);
            $('table').find('.toform').removeClass('toform');

            var child = $(this).find('.child_dblcl');

            var text = child.text();
            var model = child.attr('model');
            var id = child.attr('id');
            var field = child.attr('name');
            var editor = child.attr('editor');
            //alert(id);
            //$(this).removeClass('dblcl');
            //if ( !$(this).hasClass('toform') ) {
            if (editor == "true") {
                child.addClass('toform').html('<form method="post" action="/dmn/'+model+'/fastedit/"><input type="hidden" name="Fastedit_field" value="'+field+'" /><input type="hidden" name="Fastedit_id" value="'+id+'" /><textarea class="form" id="cleditor" name="Fastedit_text" rows=5 cols=3>'+child.html()+'</textarea><br><input type="submit" value="ok!"></form>');
            }
            else {
                child.addClass('toform').html('<form method="post" action="/dmn/'+model+'/fastedit/"><input type="hidden" name="Fastedit_field" value="'+field+'" /><input type="hidden" name="Fastedit_id" value="'+id+'" /><textarea class="form" name="Fastedit_text" rows=5 cols=3>'+child.html()+'</textarea><br><input type="submit" value="ok!"></form>');
            }
            //}
            //$(this).removeClass('toform'); 
            //$("#cleditor").cleditor();
            $("#cleditor").cleditor({
                        width:        250,
                        height:       250
            });
        }
    });

    /* Create/Update
    ================================================== */
    //Images
    $('.im2').toggle(
        function() {
            $('.getim2').fadeOut();
            $(this).siblings('.getim2').fadeIn();
        },
        function() {
            $('.getim2').fadeOut();
            $(this).siblings('.getim2').fadeOut();
        }
    );

     /* Upload Gallery
    ================================================== */
    //Images
    /*
    function ftooltipe(){
        $(".more_inf img[title]").tooltipe({
                predelay: 300
        });
    }

    ftooltipe();
    */
    

            

    $(".aj_del_attach").live("click", function(){
        var id = $(this).attr('name');
        $.ajax({
           type: "GET",
           url: "/dmn/aj_del_attach/",
           data: "dattach_id="+id,
           success: function(msg){
             if ( msg = 'ok' ){
                $('.iformset_remove_'+id).remove();
            }
           }
         });
    });

    $('.context').live('contextmenu', function(e) {
        e.preventDefault;
        var context_id = $(this).attr('name');
        //alert('.context_id_'+context_id)
        $('.dropdown-menu').css('display', 'none');
        $('ul.context_id_'+context_id).fadeIn();
        //alert('The eventhandler will make sure, that the contextmenu dosnt appear.');
        $('ul.context_id_'+context_id).hover(
            function(){
            $(this).css('display', 'block');
            },
            function(){
                $(this).fadeOut();
            }
        );
        return false;
    });

    

    /* Ajax Form submit
    ================================================== */
    //var test = $('.test');

    $('form.createup').ajaxForm({
                beforeSerialize:function($Form, options){
                    /* Before serialize */
                    if (typeof(CKEDITOR) != 'undefined') {
                            for ( instance in CKEDITOR.instances ) {
                                CKEDITOR.instances[instance].updateElement();
                            }
                            return true; 
                        }
                    },
                beforeSend: function() {
                },
                uploadProgress: function(event, position, total, percentComplete) {
                },
                complete: function(xhr) {
                    if (xhr.status == 200) {
                        window.location.href = xhr.getResponseHeader('Location')
                        // console.log(xhr)
                    }
                    else {
                        // console.log(xhr)
                        var obj = jQuery.parseJSON(xhr.responseText);
                        // console.log(obj['field_errors']);
                        $('input').removeClass('bord_red');
                        for (x in obj['errors']) {
                            generate('error', '<b>'+x+'</b>: <i>'+obj['errors'][x]+'</i>');
                        }
                        for (x in obj['field_errors']) {
                            $('#id_'+obj['field_errors'][x]).addClass('bord_red');
                        }
                    }
                }
            });








    

});