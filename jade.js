var fs = require('fs');
var extname = require('path').extname;
var jade = require('jade');
var fn = jade.compileFile('index.jade',{});

var root='d:/xue/6.041';

fs.readdir(root,function(err,files){
    if(err) return;
    var videos =  files.filter(function(e){
        return extname(e) == '.mp4'
    });
    var html = fn({videos: videos}) ;
    fs.writeFile('index.html',html);
        
});



// // template index.jade
// html
//   body
//     #player(style="left: 0px; top: 0px;")
//       video(controls, preload="auto", width="1040", height="564")
//         source(src="file://e:/MIT6041XT114-G0501_100.mp4", type="video/mp4")
//     #videos(style="position: absolute; top: 0px; left: 1100px; width: 200px; height: 600px;")
//       ul
//         each val in videos
//           li(onclick='play("' + val+ '")')=val
//     script(type='text/javascript').
//       var video = document.getElementsByTagName('video')[0];
//       var source = document.getElementsByTagName('source')[0];
//       function play(name){
//       source.src = 'file://d:/xue/6.041/' + name;
//       video.load()
//       video.play()
//       }

    

