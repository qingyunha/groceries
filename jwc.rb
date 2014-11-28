#! /usr/bin/env ruby
require 'net/http'


uri1 = URI('http://202.207.177.15:7777/pls/wwwbks/bks_login2.login')
req1 = Net::HTTP::Post.new(uri1.path)

#uri2 = URI('http://202.207.177.15:7777/pls/wwwbks/bks_login2.loginmessage')
#req2 = Net::HTTP::Get.new(uri2.request_uri)


stuid = ARGV[0]
pwd = ARGV[1]
req1.set_form_data('stuid' => stuid, 'pwd' => pwd)

Net::HTTP.start(uri1.hostname, uri1.port) do |http|
      
  if http.request(req1).is_a? Net::HTTPRedirection
    puts "your passwd is #{pwd}"
  else
    puts "wrong password"
  end
end
 
