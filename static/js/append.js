var socket = null;
var socket_close = false;
var socket_param = [];

function connect_ws(url, fnc_open, fnc_close, fnc_message) {
	socket_param = [];
	socket_param.push(url);
	socket_param.push(fnc_open);
	socket_param.push(fnc_close);
	socket_param.push(fnc_message);
	socket_close = false;
	try {
		socket = new WebSocket(`${url}/socket`);
	} catch (e) {
		socket_close = true;
		set_message("alert", `${url} に対するWebSocket通信に失敗しました。`);
		stop_loading();
	}
	socket.onerror = function() {
		socket_close = true;
		set_message("alert", `${url} に対するWebSocket通信に失敗しました。`);
		stop_loading();
	};

	if (fnc_open != null) {
		socket.onopen = fnc_open;
	}
	socket.onclose = function() {
		if (!socket_close) {
			try {
				connect_ws(url, fnc_open, fnc_close, fnc_message);
				return;
			} catch (ex) {
				set_message("alert", ex.message);
				stop_loading();
			}
		}
		if (fnc_close != null) {
			fnc_close();
		}
		socket = null;
		stop_loading();
	};
	if (fnc_message != null) {
		socket.onmessage = function(message) {
			var data = JSON.parse(message.data);
			fnc_message(data);
		};
	}
}

function close_ws() {
	socket_close = true;
	if (socket != null) {
		socket.close();
		socket = null;
	}
}

function send_ws(data) {
	try {
		socket.send(JSON.stringify(data));
	} catch (e) {
		close_ws();
		set_message("alert", "サーバーとの接続が切断されました。\n" + e.message);
	}
}

function change_form_type(id) {
	var frm = document.getElementById(id);
	if (frm.type === "password") {
		frm.type = "text";
	} else {
		frm.type = "password";
	}
}

function view_loading() {
	var h = $(window).height();
	$('#loading').css('display','block').css('height',h);
}

function stop_loading() {
	$('#loading').css('display','none');
}

function clear_message() {
	lst_message_type.forEach(function(key) {
		$(`#div_message_${key}`).hide();
		$(`#div_message_${key}_text`).html("");
	});
}

function set_message(message_type, message) {
	clear_message();
	$(`#div_message_${message_type}`).show();
	$(`#div_message_${message_type}_text`).html(message);
}

async function copy2clipboard (val) {
	const queryOpts = { name: 'clipboard-read', allowWithoutGesture: false };
	const permissionStatus = await navigator.permissions.query(queryOpts);
	permissionStatus.onchange = () => {
		if (navigator.clipboard) {
			navigator.clipboard.writeText(val).then(
				() => { },
				() => { }
			);
		}
	}
}
