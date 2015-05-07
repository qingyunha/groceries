var http = require('http');
var parse = require('url').parse;

var server = http.createServer(function(request,respose){
    console.log(request.url);
    var url = parse(request.url);
    request_opt = {
        hostname : url.hostname,
        port : url.port,
        path : url.path,
        method : request.method,
        headers : request.headers
    }
    console.log(request_opt);
    console.log('**************************************************');
    var proxy = http.request(request_opt,function(res){
        res.pipe(respose);
    });
    proxy.on('error',function(e){console.log(e.message)})
    proxy.end();//***必不可少***
}).listen(8080);
