require 'net/http'

uri = URI("http://www.ip.cn")
p1 = /<code>(?<ip>.*)<\/code>/
p2 = /<p>GeoIP: (?<addr>.*)<\/p>/

loop do
  res = Net::HTTP.get_response uri
  html = res.body
  ip = p1.match(html)['ip']
  addr = p2.match(html)['addr']
  print Time.now.to_s[0..18] + ": " +ip + " " + addr + "\n"
  sleep 3600 
end
