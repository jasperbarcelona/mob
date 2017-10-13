householdsSearchStatus = 'off'

function supply_household_data(household_id){
  $.get('/household',{
    household_id:household_id
  },
  function(data){
    $('#edit-household-modal').find('.modal-title').html(data['household_name']);
    $('#edit-household-modal').find('.modal-body').html(data['template']);
  });
}

function toggle_search(){
  tab = 'households';
  if ((typeof eval(tab+'SearchStatus') === 'undefined') || (eval(tab+'SearchStatus') == 'off')){
        $('#'+tab+'-search-panel').show();
        /*$('#search-loading').show();*/
        $('#'+tab).removeClass('maximized');
        $('#'+tab).addClass('minimized');
        window[tab+'SearchStatus'] = 'on';
    }
    else{
        $('#'+tab+'-search-panel').hide();
        $('#search-loading').hide();
        $('#'+tab).addClass('maximized');
        $('#'+tab).removeClass('minimized');
        $('#'+tab+'-search-panel .search-text').val('');
        $('#'+tab+'-search-panel .search-option').val('');
        window[tab+'SearchStatus'] = 'off';
        window[tab+'_result'] = false;
        back_home();
    }
}