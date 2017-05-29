//var sql = window.require('sql.js');

function loadDBfile(){
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "../test.db", true);
	xhr.responseType = 'arraybuffer';


	xhr.onload() = function(e){
		var uInt8Array = new uInt8Array(this.response);
		var db = new SQL.Database(uInt8Array);
		var contents = db.exuc("SELECT * FROM POSTS");
		document.write("hello!\n");
		document.write(contents);
	

	};

	xhr.send();
}

