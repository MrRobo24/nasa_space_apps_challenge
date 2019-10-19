from firebase import firebase
firebase = firebase.FirebaseApplication('https://helloworld-252113.firebaseio.com/', None)
result = firebase.get('/users', None)
print(result)