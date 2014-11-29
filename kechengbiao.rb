#! /usr/bin/env ruby
require 'net/http'
require 'nokogiri'
require 'writeexcel'


class KC
  attr_reader :res, :schedule

  def initialize id, psw
    @id, @psw = id, psw
  end


  def start
    uri1 = URI('http://www1.nuc.edu.cn/jwc/jwyx/kbcx/customer/check_chkadmin1.asp')
    req1 = Net::HTTP::Post.new(uri1.path)
    req1.set_form_data('duixiang' => 'stu', 'users' => @id, 'psw' => @psw)

    uri2 =  URI('http://www1.nuc.edu.cn/jwc/jwyx/kbcx/customer/out.asp')
    req2 = Net::HTTP::Get.new(uri2.path)

    Net::HTTP.start(uri1.hostname, uri1.port) do |http|
      
      res = http.request req1
      if res['location'] == 'out.asp'
        req2['cookie'] = res['set-cookie']
        @res = http.request req2
        'ok'
      else
        puts "wrong password"
      end
    end
  end

  def generate
    start if not @res
    @schedule = []
    7.times {|i|  @schedule[i] = []}

    table = Nokogiri::HTML(@res.body).css('table')[1]
    table.css('tr').each_with_index do |e,i|
      next if i == 0
      if i % 2 == 1
        e.css('td').each_with_index do |t,j|
          next if j < 2
          @schedule[j-2] << t.content
        end
      else
        e.css('td').each_with_index do |t,j|
          next if j < 1
          @schedule[j-1] << t.content
        end
      end
    end
    'ok'
  end

  def generate_excel
    generate if not @schedule
    book = WriteExcel.new 'schedule.xls'
    s = book.add_worksheet
    @schedule[0..4].each_with_index do |c, i|
      s.write(0,i,i+1)
      c.each_with_index { |a_class, j|
        s.write(j+1, i, a_class)
      }
    end
    book.close
    'ok'
  end
end

if __FILE__ == $0
  (k = KC.new(ARGV[0],ARGV[1])).start
  File.open('/tmp/schedule.html','w') do |f|
    f << k.res.body
  end
end
