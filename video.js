// 做这个程序的起因：
// 我在edx上学习6.041课程，它的在线教学视频被墙了，但
// 是可以下载（在amzon的云上）。下载后的情况是我要同时打开浏览器，暴风影音，pdf，
// 并且要频繁在他们之间切换，另外暴风一起风扇狂转。我想起HTML5有个video标
// 签，这就是起因。


// 目前的问题：
// 1. 不能定点播放，不能任意点击视屏进度条的一点进行播放。
// 2. 不能重复播放。
// 3. 不能带字幕，不知道为什么track标签不起作用。（可能是由于CORS的原因）


// TODO：
// 1. 尝试高层框架如express提供的处理媒体文件的接口。 
// 2. 换一个思路，对含视频和字幕的目录动态生成HTML和JavaScript（区别是video
// 的src属性改成了file，而不是http）。 这可以解决前两个问题。（参见jade.js）



var http = require('http');
var fs = require('fs');
var join = require('path').join;
var extname = require('path').extname;
var parse = require('url').parse

root = 'd:/xue/6.041';

var server = http.createServer(function(req, res){
    url = parse(req.url)
    if(url.query){
      handler_play(url.pathname, res)
    }else{
      handler_dir(url.pathname, res)
    } 
})

function handler_play(path, res){
    html = '<html<body><video id="e1" class="video-js vjs-default-skin" controls preload="auto" width="1040" height="580" data-setup="{}"><source src="' + path + '" type="video/mp4" /><track kind="captions" src="test.vtt" srclang="en" label="English" default /></video></body></html>';
    res.end(html);
}

function handler_dir(pathname, res){
    if(pathname.match('public')){
        var path = join(__dirname, pathname)
    }else{
        var path = join(root, pathname)
    }
    fs.stat(path, function(err,stats){
        if(err){
            res.end('inter error');
        }else{
            if(stats.isDirectory()){
                render_dir(path);
            }else{
                res.setHeader('Content-Length', stats.size);
                if(extname(path) == '.mp4') res.setHeader("Content-Type", "video/mp4");
                var stream = fs.createReadStream(path)
                stream.pipe(res);
                stream.on('error', function(err){
                    res.end();
                })
            }}})
    function render_dir(path){
        fs.readdir(path, function(err, files){
            if(err){
                res.end('inter err');
            }else{
                var html = '<html><body>';
                for(var i in files){
                    if(extname(files[i]) == '.mp4'){
                        html = html + '<a target="_blank" href="' + join( pathname, files[i]) + '?action=play">' + files[i] + '</a><br/>';
                    }else{
                        html = html + '<a target="_blank" href="' +join( pathname, files[i]) + '">' + files[i] + '</a><br/>';
                    }
                }
                html = html + '</body></html>';
                res.end(html);
            }
            
        })
    }
}


server.listen(8888)
