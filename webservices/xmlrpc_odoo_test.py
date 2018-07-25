import functools
import xmlrpc.client
HOST = 'localhost'
PORT = 8069
DB = 'odoo-test'
USER = 'hector@benandfrank.com'
PASS = 'cuatroojos?'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

# 1. Login
uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print("Logged in as %s (uid:%d)" % (USER,uid))

call = functools.partial(
    xmlrpc.client.ServerProxy(ROOT + 'object').execute,
    DB,
    uid,
    PASS
)

# 2. Read the session
sessions = call('openacademy.session', 'search_read', [], ['name', 'seats', 'course_id'])
for session in sessions:
    print("Session %s (%s seats) %s" % (session['name'], session['seats'], session['course_id']))

# 3. Create a new session
session_id = call('openacademy.session', 'create', {
    'name' : 'My session',
    'course_id' : 2,
})

course_id = call('openacademy.course', 'search', [('name','ilike','The art of dealing with womens')])[0]
session_id = call('openacademy.session', 'create', {
    'name' : 'My session assigned',
    'course_id' : course_id,
})
