angular['module']('json', ['ngCookies'])['controller']('loginController', ['$http', '$scope', '$cookies', function(req, _0x30f6x2, _0x30f6x3) {
	    _0x30f6x2['credentials'] = {
		            UserName: '',
		            Password: ''
		        };
	    _0x30f6x2['error'] = {
		            message: '',
		            show: false
		        };
	    var auth = _0x30f6x3['get']('OAuth2');
	    if (auth) {
		            window['location']['href'] = 'index.html'
		        };
	    _0x30f6x2['login'] = function() {
		            req['post']('/api/token', _0x30f6x2['credentials'])['then'](function(_0x30f6x5) {
				                window['location']['href'] = 'index.html'
				            }, function(_0x30f6x6) {
						                _0x30f6x2['error']['message'] = 'Invalid Credentials.';
						                _0x30f6x2['error']['show'] = true;
						                console['log'](_0x30f6x6)
						            })
		        }
}])['controller']('principalController', ['$http', '$scope', '$cookies', function(req, _0x30f6x2, _0x30f6x3) {
	    var auth = _0x30f6x3['get']('OAuth2');
	    if (auth) {
		            req['get']('/api/Account/', {
				                headers: {
							                "Bearer": auth
							            }
				            })['then'](function(_0x30f6x5) {
						                _0x30f6x2['UserName'] = _0x30f6x5['data']['Name']
						            }, function(_0x30f6x6) {
								                _0x30f6x3['remove']('OAuth2');
								                window['location']['href'] = 'login.html'
								            })
		        } else {
				        window['location']['href'] = 'login.html'
				    }
}])
