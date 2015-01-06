require 'rainbow/ext/string'

bn = File.basename ARGV[0], '.mp3'
su = bn + '.lrc'

player = Thread.new {
  `mpg123 #{ARGV[0]}` 
}

ftime = 0
File.open(su).each_line do |line|
  time = line[1..8]
  min, sec = time.split ':' 
  time = min.to_i * 60 + sec.to_f
  sleep time - ftime
  print line[10..-1].color(:green)
  ftime = time
end

play.join


if __FILE__ == $0
  gem 'minitest'
  require 'minitest/autorun'

  class TestPlay < Minitest::Test
     def test_time
        skip
     end
  end
end
