require 'rainbow/ext/string'

bn = File.basename ARGV[0], '.mp3'
su = bn + '.lrc'

mpgpid = fork {
  `mpg123 #{ARGV[0]}` 
}

subpid = fork { 
  ftime = 0
  File.open(su).each_line do |line|
    time = line[1..8]
    min, sec = time.split ':' 
    time = min.to_i * 60 + sec.to_f
    sleep time - ftime
    print line[10..-1].color(:green)
    ftime = time
  end
} 

sleep 1  #make sure mpg123 has already run
mpgpid = `ps u | grep mpg123`.split[1]
sig = 0
Signal.trap('TSTP'){
  if sig == 0
    Process.kill(:TSTP, subpid.to_i)
    Process.kill(:TSTP, mpgpid.to_i)
    sig = 1
  else
    Process.kill(:CONT, mpgpid.to_i)
    sleep 1.5 #try to synchronize mpg and subtitle
    Process.kill(:CONT, subpid.to_i)
    sig = 0
  end
}
sleep

if __FILE__ == $0
  gem 'minitest'
  require 'minitest/autorun'

  class TestPlay < Minitest::Test
     def test_time
        skip
     end
  end
end
