
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
    keystone.fiware_roles.roles.update(role1, name='Role Cool Test')
    print('\n Roles list (after updating the name of role 1): \n')
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
    keystone.fiware_roles.permissions.update(permission1, name='Permission Cool Test')
    print('\n Permission list (after updating the name of permission 1):  \n')
    print keystone.fiware_roles.permissions.list()
    print('\n Permission list (after deleting permission 2): \n')
    keystone.fiware_roles.permissions.delete(permission2_id)
    print keystone.fiware_roles.permissions.list()

    keystone.fiware_roles.permissions.delete(permission1_id)

#Roles-Permissions relation
if 0:
    role1 = keystone.fiware_roles.roles.create(name='Role Test 1')
    role1_id = role1.id
    permission1 = keystone.fiware_roles.permissions.create(name='Permission Test 1')
    permission1_id = permission1.id
    permission2 = keystone.fiware_roles.permissions.create(name='Permission Test 2')
    permission2_id = permission2.id

    keystone.fiware_roles.permissions.add_role(role1, permission1)
    print('\n Permissions that belong to role 1: \n')
    print keystone.fiware_roles.permissions.list(role=role1)

    keystone.fiware_roles.permissions.add_role(role1, permission2)
    print('\n Permissions that belong to role 1 (after adding permission 1 and 2): \n')
    print keystone.fiware_roles.permissions.list(role=role1)

    keystone.fiware_roles.permissions.remove_role(role1, permission1)
    print('\n Permissions that belong to role 1 (after removing permission 1): \n')
    print keystone.fiware_roles.permissions.list(role=role1)

    keystone.fiware_roles.permissions.add_role(role1, permission1)
    keystone.fiware_roles.permissions.delete(permission1)
    print('\n Permissions that belong to role 1 (after deleting permission 1): \n')
    print keystone.fiware_roles.permissions.list(role=role1)

    keystone.fiware_roles.roles.delete(role1_id)
    keystone.fiware_roles.permissions.delete(permission2_id)

#Roles-Users relation
if 0:
    role1 = keystone.fiware_roles.roles.create(name='Role Test 1')
    role1_id = role1.id
    role2 = keystone.fiware_roles.roles.create(name='Role Test 2')
    role2_id = role2.id

    organization= keystone.projects.create(name='organization', domain='default')
    user = keystone.users.create(name='user',password='user',project=organization)

    keystone.fiware_roles.roles.add_user(role1, user, organization)
    print('\n Roles that belong to user: \n')
    print keystone.fiware_roles.roles.list(user=user)

    keystone.fiware_roles.roles.add_user(role2, user, organization)
    print('\n Roles that belong to user (after adding role 1 and 2 to user): \n')
    print keystone.fiware_roles.roles.list(user=user)

    keystone.fiware_roles.roles.remove_role(role1, user, organization)
    print('\n Roles that belong to user (after removing role 1): \n')
    print keystone.fiware_roles.roles.list(user=user)

    keystone.fiware_roles.roles.add_user(role1, user)
    keystone.fiware_roles.roles.delete(role1)
    print('\n Roles that belong to user (after deleting role 1): \n')
    print keystone.fiware_roles.roles.list(user=user)


    keystone.fiware_roles.roles.delete(role2)
    keystone.projects.delete(organization)
    kesytone.users.delete(user)
