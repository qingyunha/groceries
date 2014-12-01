require 'socket'
require 'uri'

class Serve
  OK = "HTTP/1.0 200 Okay\r\nServer: k\r\nContent-Type: text/html\r\n\r\n"
  
  def initialize(port)
    @listener = TCPServer.new port
    @dispatch_table = Hash.new
  end
  
  def run
    loop do
       Thread.start(@listener.accept) do |client|
           print "request from" + client.peeraddr.inspect + "\n" 
           handle client
           client.close
       end.join
    end
  end
  
  def handle client
    req = /GET (?<url>.+) HTTP\/[0-9]\.[0-9]/.match(client.readline)[:url]
    puts "requst url is #{req}"
    req = URI(req)
    res = dispatch req
    client.write res
  end
  
  def dispatch req
    if handler = @dispatch_table[req.path]
       OK + handler.call(req)
     else
       OK + "<html><head></head><body>error page<body></html>"
     end
  end
  
  def add_serverlet pattern, method
    @dispatch_table[pattern] = method
  end
end



handle_many = Proc.new { |req|
 build_form_page("Number of greetings:","/reply","")
}

handle_reply = Proc.new{ |req|
 number = req.query.split('&').grep(/number/)[0].match(/\d+/)[0].to_i
 "hello " * number
}

handle_sum = Proc.new{|req|
  build_form_page "First number:", "/one", ""
}

handle_one = Proc.new{|req|
  number = req.query.split('&').grep(/number/)[0].match(/\d+/)[0]
  build_form_page "Second number:", "/two", number
}

handle_two = Proc.new{|req|
  query = req.query.split('&');
  number1 = query.grep(/hidden/)[0].match(/\d+/)[0].to_i
  number2 = query.grep(/number/)[0].match(/\d+/)[0].to_i
  "<p>the sum is #{number1 + number2}</p>"
}


#help function
require 'haml'

def build_form_page label, next_url, hidden
  tempt = %{
%html
  %head
    %title
      "Enter a Number to Add"
  %body{:bgcolor => "white"}
    %form{:action => "#{next_url}", :method => "GET"}
      #{label}
      %input{:type => "text", :name => "number", :value => ""}
      %input{:type => "hidden", :name => "hidden", :value => "#{hidden}"}
      %input{:type => "submit", :name => "enter", :value => "Enter"}
}
  Haml::Engine.new(tempt).render

end


@server = Serve.new 8001
@server.add_serverlet('/many', handle_many)
@server.add_serverlet('/reply', handle_reply)
@server.add_serverlet('/sum', handle_sum)
@server.add_serverlet('/one', handle_one)
@server.add_serverlet('/two', handle_two)
@server.run




