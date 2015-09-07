var myScroll;
var scroll_distance = 0;
var old_scroll_y = 0;

var BASE_PATH = "../cgi-bin";
//var BASE_PATH = "../cgi-bin";

function getImage(type) {
	if(type == "back") {
		return "ui-icon-back"
	} else if(type == "Settings") {
		return "ui-icon-gear"
	} else if(type == "Power") {
		return "ui-icon-power"
	} else if(type == "Load") {
		return "ui-icon-refresh"
	} else if(type == "Dispense") {
		return "ui-icon-arrow-d"
	} else if(type == "Schedule") {
		return "ui-icon-calendar"
	} else if(type == "Schedules") {
		return "ui-icon-calendar"
	} else if(type == "WIFI") {
		return "ui-icon-cloud"
	} else if(type == "New") {
		return "ui-icon-plus"
	} else if(type == "Users") {
		return "ui-icon-user"
	}
}

function addButton(type) {
	var image = getImage(type);
	var $newdiv1 = $( '<div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn '+image+' ui-btn-icon-bottom ui-mini" onclick="loadPage(\''+type+'\');">'+type+'</a></div>' );
	$("#grid").append($newdiv1);
}

function addUserButton(user) {
	var $newdiv1 = $( '<div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-user ui-btn-icon-bottom ui-mini" onclick="loadUserMeds(\''+user+'\');">'+user+'</a></div>' );
	$("#grid").append($newdiv1);
}
function addManageUserButton(user) {
	if(user == "New") {
		var $newdiv1 = $( '<div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-plus ui-btn-icon-bottom ui-mini" onclick="loadUserManager(\''+user+'\');">'+user+'</a></div>' );
	} else {
		var $newdiv1 = $( '<div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-user ui-btn-icon-bottom ui-mini" onclick="loadUserManager(\''+user+'\');">'+user+'</a></div>' );
	}
	$("#grid").append($newdiv1);
}
function addUserScheduleButton(user) {
	var $newdiv1 = $( '<div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-user ui-btn-icon-bottom ui-mini" onclick="displaySchedules(\''+user+'\');">'+user+'</a></div>' );
	$("#grid").append($newdiv1);
}


function displaySchedule() {

	$.ajax({url:BASE_PATH+"/get_master_schedule",
			success:function(result){
				items = JSON.parse(result);

				cur_date = 0;

				for (var i = 0, len = items.length; i < len; i++) {
					if(items[i].date != cur_date) {
						$item = $('<li data-role="list-divider">'+items[i].date+'</li>');
						$("#list").append($item);
						cur_date = items[i].date;
					}
					if(items[i].as_needed == 1)
					{
						$item = $('<li><b>'+items[i].user+'</b><br>'+items[i].medname+'<p class="ui-li-aside"><strong>'+items[i].time+' (As Needed)</strong></p></li>');
					} else {
						$item = $('<li><b>'+items[i].user+'</b><br>'+items[i].medname+'<p class="ui-li-aside"><strong>'+items[i].time+'</strong></p></li>');
					}
					$("#list").append($item);
				}
				$('#list').listview().listview('refresh');
				myScroll = new IScroll("#scroll-wrapper", { probeType: 1});
					
			}
	}); 

}

function loadPage(page) {

	$("#list").empty();
	$("#grid").empty();
	$("#form_user").hide();
	$("#form_newmed").hide();
	$("#scroll-wrapper").show();

	if(page == "home") {
		setTitle("Welcome");
		addButton("Dispense");
		addButton("Load");
		addButton("Schedule");
		addButton("Power");
		addButton("Settings");
	} else if(page == "Settings") {
		setTitle("Settings");
		addButton("WIFI");
		addButton("Users");
		addButton("Medications");
		addButton("Schedules");
	} else if(page == "Power") {
		setTitle("Power");
		addButton("Shutdown");
		addButton("Restart");
		addButton("Cancel");
	} else if(page == "Shutdown") {
		shutdown();
	} else if(page == "Restart") {
		restart();
	} else if(page == "Cancel") {
		loadPage("home");
	} else if(page == "Users") {
		setTitle("Users");
		$.ajax({url:BASE_PATH+"/get_users",
			success:function(result){
				users = JSON.parse(result);

				for (var i = 0, len = users.length; i < len; i++) {
					addManageUserButton(users[i].name);
				}
				addManageUserButton("New");
  			}
		});
	} else if(page == "Dispense") {
		setTitle("Choose User");
		$.ajax({url:BASE_PATH+"/get_users",
			success:function(result){
				users = JSON.parse(result);

				for (var i = 0, len = users.length; i < len; i++) {
					addUserButton(users[i].name);
				}
  			}
		});
	} else if(page == "newmed") {
		setTitle("New Medication");
		displayNewMedForm();
	} else if(page == "Load") {
		setTitle("Load Meds");
		loadUserMeds(false, true);
	} else if(page == "Schedule") {
		setTitle("Schedule");
		displaySchedule();
	} else if(page == "Schedules") {
		setTitle("Schedules");
		$.ajax({url:BASE_PATH+"/get_users",
			success:function(result){
				users = JSON.parse(result);

				for (var i = 0, len = users.length; i < len; i++) {
					addUserScheduleButton(users[i].name);
				}
  			}
		});
	} else if(page == "WIFI") {
		setTitle("WiFi Settings");
		displayWIFI();
	} else if(page == "Medications") {
		setTitle("Manage Medications");
		manageMedications();
	}
}

function setTitle(name) {
	$("#headtitle").empty();
	$("#headtitle").append(name);
}

function displayWIFI() {
	$("#grid").empty();
	$.ajax({url:BASE_PATH+"/wifi_info",
		success:function(result){
			$("#grid").empty();
			$("#grid").html(result);
  		}
	});
}

function shutdown() {
	$("#grid").empty();
	$.ajax({url:BASE_PATH+"/shutdown",
		success:function(result){
			$("#grid").empty();
			$("#grid").html(result);
  		}
	});
}

function restart() {
	$("#grid").empty();
	$.ajax({url:BASE_PATH+"/restart",
		success:function(result){
			$("#grid").empty();
			$("#grid").html(result);
  		}
	});
}

function vendConfirm(id, name, user) {
	if(scroll_distance < 2 && scroll_distance > -2) { //make sure we weren't scrolling
		$("#list").empty();
		$("#grid").empty();
		var $newdiv1 = $( '<center><br>Vend '+name+' for '+user+'<br><br></center><div class="ui-block-b"></div><div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-plus ui-btn-icon-bottom ui-mini" onclick="vend(\''+id+'\', \''+user+'\');">Vend</a></div>' );
		$("#grid").append($newdiv1);
	}
}

function loadConfirm(id, name, user) {
	if(scroll_distance < 2 && scroll_distance > -2) { //make sure we weren't scrolling
		$("#list").empty();
		$("#grid").empty();
		$("#grid").html("<center><br><br>Please Wait...<br>");
		$.ajax({url:BASE_PATH+"/load_meds",
			data: { user: user, med: id, mode: "move" },
			success:function(result){
				$("#grid").empty();
				$("#grid").html("<center><br>Insert 1 pill and press \"Load\" below.<br><br></center>");
				var $newdiv1 = $( '<div class="ui-block-b"></div><div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-plus ui-btn-icon-bottom ui-mini" onclick="load(\''+id+'\',\''+user+'\', \'insert\');">Load</a></div>' );
				$("#grid").append($newdiv1);
  			}
		});
	}
}

function vend(id, user) {
	$("#grid").empty();
	$("#grid").html("<center><br><br>Vending...");
	$.ajax({url:BASE_PATH+"/vend_meds", 
		data: { user: user, med: id },
		success:function(result){
			$("#grid").html(result);
		}
	});
	// save in log
	$.ajax({url:BASE_PATH+"/add_log", 
		data: { user: user, med_id: id , consumed: 1},
		success:function(result){
			loadPage('home');
		}
	});
}

function load(id, user, mode) {
	$("#grid").empty();
	if(mode == "insert"){
		$("#grid").html("<center><br><br>Please Wait...");
		$.ajax({url:BASE_PATH+"/load_meds",
			data: { user: user, med: id, mode: mode },
			success:function(result){
				loadPage('Load');
  			}
		});
	}
}

function displayNewMedForm() {
	$("#list").empty();
	$("#grid").empty();
	$('input[name="newmedname"]').val("");
	$('input[name="newmedbarcode"]').val("");
	$("#form_newmed").show();
	$("#scroll-wrapper").hide();
}


function loadUserManager(user) {
	$("#list").empty();
	$("#grid").empty();
	if(user == "New") {
		$('input[name="name"]').val("");
		$('input[name="weight"]').val("");
		$('input[name="month"]').val("");
		$('input[name="day"]').val("");
		$('input[name="year"]').val("");
		$("#form_sex").val("1").slider("refresh");
	} else {
		$.ajax({url:BASE_PATH+"/get_users",
			success:function(result){
				users = JSON.parse(result);

				for (var i = 0, len = users.length; i < len; i++) {
					if(users[i].name == user) {
						$('input[name="name"]').val(users[i].name);
						$('input[name="weight"]').val(users[i].weight);
						$('input[name="month"]').val(users[i].month);
						$('input[name="day"]').val(users[i].day);
						$('input[name="year"]').val(users[i].year);
						$("#form_sex").val(users[i].sex).slider("refresh");
					}
				}
  			}
		});
	}
	$("#form_user").show();
	$("#scroll-wrapper").hide();
}

function submitUserForm() {
	$("#grid").empty();
	$.ajax({url:BASE_PATH+"/add_user", 
		data: $('#form_user').serialize(),
		success:function(result){
			$( ".ui-loader" ).loader( "hide" );
			loadPage('Users');
		}
	});
}

function submitNewMedForm() {
	$("#grid").empty();
	$.ajax({url:BASE_PATH+"/add_med", 
		data: $('#form_newmed').serialize(),
		success:function(result){
			$( ".ui-loader" ).loader( "hide" );
			loadPage('home');
		}
	});
}

function submitScheduleForm() {
	$("#grid").empty();
	$.ajax({url:BASE_PATH+"/add_schedule", 
		data: $('#form_schedule').serialize(),
		success:function(result){
			$( ".ui-loader" ).loader( "hide" );
			loadPage('Settings');
		}
	});
}

function deleteMed(id) {
	$("#grid").empty();
	$.ajax({url:BASE_PATH+"/delete_med", 
		data: "id="+id,
		success:function(result){
			loadPage('Medications');
		}
	});
}


function loadUserMeds(user, add) {
	var meds = [];
	if(add)
		url = BASE_PATH+"/get_meds_all";
	else
		url = BASE_PATH+"/get_meds";

	$.ajax({url:url,success:function(result){
		meds = JSON.parse(result);

		$("#grid").empty();

		if(add) {
			$meds = $('<li class="ui-li-has-count ui-last-child"><a href="#" class="ui-btn ui-btn-icon-right ui-icon-carat-r" onclick="loadPage(\'newmed\')">New Medication <span class="ui-li-count ui-body-b">+</span></a></li>');
			$("#list").append($meds);
		}

		for (var i = 0, len = meds.length; i < len; i++) {
			if(add) {
				$meds = $('<li class="ui-li-has-count ui-last-child"><a href="#" class="ui-btn ui-btn-icon-right ui-icon-carat-r" onclick="loadConfirm('+meds[i].id+',\''+meds[i].name+'\',\''+user+'\');">'+meds[i].name+'<span class="ui-li-count ui-body-b">'+meds[i].available+'</span></a></li>');
			} else {		
				$meds = $('<li class="ui-li-has-count ui-last-child"><a href="#" class="ui-btn ui-btn-icon-right ui-icon-carat-r" onclick="vendConfirm('+meds[i].id+',\''+meds[i].name+'\',\''+user+'\');">'+meds[i].name+'<span class="ui-li-count ui-body-b">'+meds[i].available+'</span></a></li>');
			}
			$("#list").append($meds);
		}
	
		myScroll = new IScroll("#scroll-wrapper", { probeType: 1});
		myScroll.on('scroll', scrolling);
		myScroll.on('beforeScrollStart', scrollStart);
  	}});

}

function manageMedications() {
	var meds = [];
	$.ajax({url:BASE_PATH+"/get_meds_all",success:function(result){
		meds = JSON.parse(result);

		$("#grid").empty();

		for (var i = 0, len = meds.length; i < len; i++) {
			$meds = $('<li class="ui-li-has-count ui-last-child"><a href="#" class="ui-btn ui-btn-icon-right ui-icon-carat-r" onclick="manageMed('+meds[i].id+',\''+meds[i].name+'\');">'+meds[i].name+'</a></li>');
			$("#list").append($meds);
		}
	
		myScroll = new IScroll("#scroll-wrapper", { probeType: 1});
		myScroll.on('scroll', scrolling);
		myScroll.on('beforeScrollStart', scrollStart);
  	}});
}

function displaySchedules(user) {
	var items = [];
	$.ajax({url:BASE_PATH+"/get_meds_all",success:function(result){
		items = JSON.parse(result);

		$("#grid").empty();

		//$item = $('<li class="ui-li-has-count ui-last-child"><a href="#" class="ui-btn ui-btn-icon-right ui-icon-carat-r" onclick="editSchedule(0,\'New\');">New Schedule Item</a></li>');
		//$("#list").append($item);

		for (var i = 0, len = items.length; i < len; i++) {
			$item = $('<li class="ui-li-has-count ui-last-child"><a href="#" class="ui-btn ui-btn-icon-right ui-icon-carat-r" onclick="editSchedule('+items[i].id+',\''+items[i].name+'\');">'+items[i].name+'</a></li>');
			$("#list").append($item);
		}
		$('#form_schuser').val(user);
	
		myScroll = new IScroll("#scroll-wrapper", { probeType: 1});
		myScroll.on('scroll', scrolling);
		myScroll.on('beforeScrollStart', scrollStart);
  	}});
}

function editSchedule(id,name) {
	if(scroll_distance < 2 && scroll_distance > -2) { //make sure we weren't scrolling
		$("#list").empty();
		$("#grid").empty();
		$("#form_schedule").show();
		$('#form_schmed').val(id);
		$('#form_schmedname').val(name);
		//TODO: $('#form_schid').value = ???;
		$("#scroll-wrapper").hide();

	}
}

function updateScheduleAlert(data) {
	$("#list").empty();
	$("#grid").empty();
	$("#grid").html("<center><br><br>"+data[0].user+": It's time to take "+data[0].medname+"<br>");
	var $newdiv1 = $( '<div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-plus ui-btn-icon-bottom ui-mini" onclick="vendConfirm(\''+data[0].med+'\', \''+data[0].medname+'\', \''+data[0].user+'\');">Vend</a></div>' );
	$("#grid").append($newdiv1);
	var $newdiv1 = $( '<div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-cloud ui-btn-icon-bottom ui-mini" onclick="snoozeScheduledVend();">Snooze</a></div>' );
	$("#grid").append($newdiv1);
	var $newdiv1 = $( '<div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-minus ui-btn-icon-bottom ui-mini" onclick="cancelScheduledVend(\''+data[0].med+'\', \''+data[0].user+'\');">Cancel</a></div>' );
	$("#grid").append($newdiv1);

}

function snoozeScheduledVend() {
	loadPage('home');
}

function cancelScheduledVend(id, user) {
	// save in log
	$.ajax({url:BASE_PATH+"/add_log", 
		data: { user: user, med_id: id , consumed: 0},
		success:function(result){
			$("#grid").html(result);
			loadPage('home');
		}
	});
}

function manageMed(id, name) {
	if(scroll_distance < 2 && scroll_distance > -2) { //make sure we weren't scrolling
		$("#list").empty();
		$("#grid").empty();
		$("#grid").append('<center><div><br>'+name+'<br><br></div></center>');
		var $newdiv1 = $( '<div class="ui-block-b"></div><div class="ui-block-b"><a href="#" class="ui-input-btn ui-btn ui-icon-minus ui-btn-icon-bottom ui-mini" onclick="deleteMed(\''+id+'\', \''+name+'\');">Delete</a></div>' );
		$("#grid").append($newdiv1);
	}
}

function scrollStart() {
	scroll_distance = 0;
	old_scroll_y = myScroll.y;
}
function scrolling() {
	scroll_distance = myScroll.y - old_scroll_y;
}

(function checkSchedule(){
   setTimeout(function(){
      $.ajax({ url:BASE_PATH+"/check_schedule", success: function(result){
		data = JSON.parse(result);
		updateScheduleAlert(data);

        //Setup the next poll recursively
        checkSchedule();
      }});
  }, 60000); //60 seconds
})();

window.onload = function() {
	$.ajax({ url:BASE_PATH+"/startup",
		success: function(data){},
		dataType: "json",
		complete: function(data) {
			// play message after init
			$.ajax({ url:BASE_PATH+"/play_message", 
			data: "message=machine ready",
			success: function(data){}, dataType: "json"});
		}
	});

	loadPage("home");

	$('#form_medbarcode')
	.keyboard({
		layout: 'custom',
		customLayout: {
			'default' : [
				'1 2 3 {sp:1} {sp:1}',
				'4 5 6 {sp:1} {sp:1}',
				'7 8 9 {sp:1} {sp:1}',
				'{sp:1} {sp:1} {sp:1} 0 {sp:1} {bksp} {accept}'
			]
		},
		maxLength : 13,
		restrictInput : true, // Prevent keys not in the displayed keyboard from being typed in
		useCombos : false // don't want A+E to become a ligature
	});

	$('#form_medname').keyboard({
	display: {
		'bksp'   :  "\u2190",
		'default': 'ABC',
		'meta1'  : '.?123',
		'meta2'  : '#+='
	},
	visible: function(e, kb, el) {
        if (kb.$preview.caret().start === 0) {
            kb.shiftActive = true;
            kb.showKeySet(el);
        }
    },
    change: function(e, kb, el) {
        var caret = kb.$preview.caret(),
            end = caret.end - 2 >= 0 ? caret.end - 2 : caret.end; 
            str = kb.$preview.val().substring(end, caret.end);
        kb.shiftActive = (caret.start === 0 || str.indexOf('. ') >= 0);
        kb.showKeySet(el);        
    }, 
	layout: 'custom',
	customLayout: {
		'default': [
			'q w e r t y u i o p {bksp}',
			'a s d f g h j k l {sp:1}',
			'{s} z x c v b n m , . {s}',
			'{meta1} {space} {meta1} {accept}'
		],
		'shift': [
			'Q W E R T Y U I O P {bksp}',
			'A S D F G H J K L {sp:1}',
			'{s} Z X C V B N M ! ? {s}',
			'{meta1} {space} {meta1} {accept}'
		],
		'meta1': [
			'1 2 3 4 5 6 7 8 9 0 {bksp}',
			'- / : ; ( ) \u20ac & @ {sp:1}',
			'{meta2} . , ? ! \' " {meta2}',
			'{default} {space} {default} {accept}'
		],
		'meta2': [
			'[ ] { } # % ^ * + = {bksp}',
			'_ \\ | ~ < > $ \u00a3 \u00a5 {sp:1}',
			'{meta1} . , ? ! \' " {meta1}',
			'{default} {space} {default} {accept}'
		]
	},
	maxLength : 30,
	});

	$('#form_name').keyboard({
	display: {
		'bksp'   :  "\u2190",
		'default': 'ABC',
		'meta1'  : '.?123',
		'meta2'  : '#+='
	},
	visible: function(e, kb, el) {
        if (kb.$preview.caret().start === 0) {
            kb.shiftActive = true;
            kb.showKeySet(el);
        }
    },
    change: function(e, kb, el) {
        var caret = kb.$preview.caret(),
            end = caret.end - 2 >= 0 ? caret.end - 2 : caret.end; 
            str = kb.$preview.val().substring(end, caret.end);
        kb.shiftActive = (caret.start === 0 || str.indexOf('. ') >= 0);
        kb.showKeySet(el);        
    }, 
	layout: 'custom',
	customLayout: {
		'default': [
			'q w e r t y u i o p {bksp}',
			'a s d f g h j k l {sp:1}',
			'{s} z x c v b n m , . {s}',
			'{meta1} {space} {meta1} {accept}'
		],
		'shift': [
			'Q W E R T Y U I O P {bksp}',
			'A S D F G H J K L {sp:1}',
			'{s} Z X C V B N M ! ? {s}',
			'{meta1} {space} {meta1} {accept}'
		],
		'meta1': [
			'1 2 3 4 5 6 7 8 9 0 {bksp}',
			'- / : ; ( ) \u20ac & @ {sp:1}',
			'{meta2} . , ? ! \' " {meta2}',
			'{default} {space} {default} {accept}'
		],
		'meta2': [
			'[ ] { } # % ^ * + = {bksp}',
			'_ \\ | ~ < > $ \u00a3 \u00a5 {sp:1}',
			'{meta1} . , ? ! \' " {meta1}',
			'{default} {space} {default} {accept}'
		]
	},
	maxLength : 9,
	});


	$('#form_weight')
	.keyboard({
		layout: 'custom',
		customLayout: {
			'default' : [
				'1 2 3 {sp:1} {sp:1}',
				'4 5 6 {sp:1} {sp:1}',
				'7 8 9 {sp:1} {sp:1}',
				'{sp:1} {sp:1} {sp:1} 0 {sp:1} {bksp} {accept}'
			]
		},
		maxLength : 3,
		restrictInput : true, // Prevent keys not in the displayed keyboard from being typed in
		useCombos : false // don't want A+E to become a ligature
	});


	$('#form_month, #form_day, #form_schmonth, #form_schday, #form_schmin, #form_schhour, #form_schrepeat')
	.keyboard({
		layout: 'custom',
		customLayout: {
			'default' : [
				'1 2 3 {sp:1} {sp:1}',
				'4 5 6 {sp:1} {sp:1}',
				'7 8 9 {sp:1} {sp:1}',
				'{sp:1} {sp:1} {sp:1} 0 {sp:1} {bksp} {accept}'
			]
		},
		maxLength : 2,
		restrictInput : true, // Prevent keys not in the displayed keyboard from being typed in
		useCombos : false // don't want A+E to become a ligature
	});

	$('#form_year, #form_schyear')
	.keyboard({
		layout: 'custom',
		customLayout: {
			'default' : [
				'1 2 3 {sp:1} {sp:1}',
				'4 5 6 {sp:1} {sp:1}',
				'7 8 9 {sp:1} {sp:1}',
				'{sp:1} {sp:1} {sp:1} 0 {sp:1} {bksp} {accept}'
			]
		},
		maxLength : 4,
		restrictInput : true, // Prevent keys not in the displayed keyboard from being typed in
		useCombos : false // don't want A+E to become a ligature
	});

}

