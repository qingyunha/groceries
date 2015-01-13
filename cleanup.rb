qeury = `gem query`

qeury.each_line do |line|
  name, versions = line.split(' ',2)
  versions =~ /\((.*)\)/
  if $1.split.size > 1
    print name,versions
    system("gem cleanup #{name}") #subshell. can't just use `gem cleanup`,the $stdout will redicted 
  end
end
