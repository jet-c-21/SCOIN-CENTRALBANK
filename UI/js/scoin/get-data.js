const SERVER = '34.206.125.65';
const PORT = 5000;

function getSCoinData()
{
    var xhr = new XMLHttpRequest();
    var url = 'http://'+SERVER+':'+PORT+'/data'
    xhr.open("GET", url, false);
	// xhr.open("GET", "http://localhost:7777/data", false);
    // xhr.open( "GET", "http://localhost:7777/");
    xhr.send(null);
    return $.parseJSON(xhr.responseText);
}

 

var sCoinData = getSCoinData();
var realTimeData = sCoinData['sc-real-time']
var hisoryData = sCoinData['sc-history'];

console.log(realTimeData);
console.log(hisoryData);