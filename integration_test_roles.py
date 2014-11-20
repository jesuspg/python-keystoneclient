
from keystoneclient.v3 import client
from keystoneclient import session
from keystoneclient.v3.contrib.oauth2 import auth
url = 'http://127.0.0.1:5000/v3'
#keystone = client.Client(token='ADMIN',endpoint=url)

keystone=client.Client(username='admin', password='secrete',
                        project_name='demo', auth_url=url)

#Basic Role Actions:
if 0:
    role1 = keystone.fiware_roles.roles.create(name='Role Test 1')
    role1_id = role1.id
    role2 = keystone.fiware_roles.roles.create(name='Role Test 2')
    role2_id = role2.id

    print('\n Get role 1: \n')
    print keystone.fiware_roles.roles.get(role1_id)
    print('\n Roles list (after updating the name of role 1): \n')
    keystone.fiware_roles.roles.update(role1, name='Role Cool Test')
    print keystone.fiware_roles.roles.list()
    print('\n Roles list (after deleting role 2): \n')
    keystone.fiware_roles.roles.delete(role2_id)
    print keystone.fiware_roles.roles.list()

    keystone.fiware_roles.roles.delete(role1_id)

#Basic Permission Actions:
if 0:
    permission1 = keystone.fiware_roles.permissions.create(name='Permission Test 1')
    permission1_id = permission1.id
    permission2 = keystone.fiware_roles.permissions.create(name='Permission Test 2')
    permission2_id = permission2.id

    print('\n Get permission 1: \n')
    print keystone.fiware_roles.permissions.get(permission1_id)
    print('\n Permission list (after updating the name of permission 1):  \n')
    keystone.fiware_roles.permissions.update(permission1, name='Permission Cool Test')
    print keystone.fiware_roles.permissions.list()
    print('\n Permission list (after deleting permission 2): \n')
    keystone.fiware_roles.permissions.delete(permission2_id)
    print keystone.fiware_roles.permissions.list()

    keystone.fiware_roles.permissions.delete(permission1_id)

#Roles-Permissions relation
if 1:
    role1 = keystone.fiware_roles.roles.create(name='Role Test 1')
    role1_id = role1.id
    role2 = keystone.fiware_roles.roles.create(name='Role Test 2')
    role2_id = role2.id
    permission1 = keystone.fiware_roles.permissions.create(name='Permission Test 1')
    permission1_id = permission1.id
    permission2 = keystone.fiware_roles.permissions.create(name='Permission Test 2')
    permission2_id = permission2.id

    keystone.fiware_roles.roles.add_permission(role1, permission1)
    print('\n Roles that belong to permission 1: \n')
    #Mirar esto porque no funciona!
    keystone.fiware_roles.roles.list(permission=permission1)


    keystone.fiware_roles.roles.delete(role1_id)
    keystone.fiware_roles.roles.delete(role2_id)
    keystone.fiware_roles.permissions.delete(permission1_id)
    keystone.fiware_roles.permissions.delete(permission2_id)