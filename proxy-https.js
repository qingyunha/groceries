/*
  使用CONNECT tunnel的https的代理服务器
  首先客户端发送CONNECT命令，指明目的服务器的主机名和端口号
  代理服务器建立与目的服务器的连接（agent-sock)
  之后，所有加密流量通过sock和agent_sock交换
*/


var net = require('net')
var https = require('https');
var fs = require('fs');


var options = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
};

var https_server = https.createServer(options, function (req, res) {
  res.writeHead(200);
  res.end("hello world\n");
})


var proxy_server = net.createServer(function(sock){
    var i = 1;
    var agent_sock
    sock.on('data', function(data){
        if(i == 1){
            /*
              收到的第一次数据，应是CONNECT命令，以这样的形式：
              CONNECT www.edx.org:443 HTTP/1.1
              Host: www.edx.org
              Proxy-Connection: keep-alive
              User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 

              所以，应该从第一行中提取主机和端口号，发起连接
             */
            
            agent_sock = net.connect({port:444});
            sock.write("HTTP/1.1 200 Connection established\r\n\r\n");
            i = 2
        }else{
            agent_sock.write(data);
        }
    });
    sock.on('error',function(e){
        console.log("client sock error: ",e);
    });
    sock.on('end',function(e){
        agent_sock.end()
    });

    
    agent_sock.on('data',function(data){
        sock.write(data)
    });
    agent_sock.on('error',function(e){
        console.log("server sock error: ",e);
    });
    agent_sock.on('end',function(e){
        sock.end()
    });
})



https_server.listen(444);

proxy_server.listen(8000);

