import os
import click
import jwt

from urllib.parse import urlparse

from typing import Tuple, Union

from dao import ClientDAO, ContractDAO, EventDAO, EmployeeDAO, DepartmentPermissionDAO, PermissionDAO, DepartmentDAO
from conf import SECRET, HOST


def find_netrc_token(machine: str, raise_errors=False):
    NETRC_FILES = (".netrc", "_netrc")
    netrc_file = os.environ.get("NETRC")
    if netrc_file is not None:
        netrc_locations = (netrc_file,)
    else:
        netrc_locations = ("~/{}".format(f) for f in NETRC_FILES)

    try:
        from netrc import netrc, NetrcParseError

        netrc_path = None

        for f in netrc_locations:
            try:
                loc = os.path.expanduser(f)
            except KeyError:
                return

            if os.path.exists(loc):
                netrc_path = loc
                break

        if netrc_path is None:
            return

        ri = urlparse(machine)

        host = ri.netloc.split(":")[0]

        try:
            _netrc = netrc(netrc_path).authenticators(host)
            if _netrc:
                login_i = 0 if _netrc[0] else 1
                return (_netrc[login_i], _netrc[2])
        except (NetrcParseError, IOError):
            if raise_errors:
                raise

    except (ImportError, AttributeError):
        pass


def read_credentials(machine: str) -> Union[Tuple[str, str], None]:
    user, token = None, None
    auth = find_netrc_token(machine, True)
    if auth and auth[0] and auth[1]:
        user = auth[0]
        token = auth[1]
        return (user, token)


def get_token_payload(token):
    return jwt.decode(token, key=SECRET, algorithms="HS256")


def get_token():
    credentials = read_credentials(HOST)
    return credentials[1]


def get_token_user_id():
    token = get_token()
    payload = get_token_payload(token)
    user = EmployeeDAO.get_by_email(payload['email'])
    return user.id


def is_authenticated(func):
    def wrapper():
        credentials = read_credentials(HOST)
        existing_token = credentials is not None
        if existing_token:
            try:
                jwt.decode(credentials[1], key=SECRET, algorithms="HS256")
                if func is not None:
                    func()
                # return True
            except jwt.ExpiredSignatureError:
                click.echo(f"Connexion expirée, connectez-vous à nouveau.")
                # return False
        # else:
        #     return False
    return wrapper

def is_allowed(func):
    allowed = "client_create"

    def wrapper(*args, **kwargs):

        if func.__name__ == ('show_all' or 'show_details'):
            func(*args, **kwargs)
        else:
            # Check which object types the user is allowed to create
            credentials = read_credentials(HOST)
            token = credentials[1]
            payload = get_token_payload(token)
            department_id = payload['department_id']
            department = DepartmentDAO.get_by_id(department_id)
            department_permissions = department.department_permissions
            employee_id = EmployeeDAO.get_by_email(payload['email']).id
            EMPLOYEE_FIELD_NAMES = {
                'contract': f"client.commercial_id={employee_id}",
                'event': f"support_contact_id={employee_id}",
                'client': f"commercial_id={employee_id}",
            }
            obj_type_allowed = [
                dpt_perm.permission.object_type
                for dpt_perm in department_permissions
                if dpt_perm.permission.crud_action == func.__name__
            ]
            if func.__name__ == 'main_menu':
                objects_allowed = list(dict.fromkeys([
                    PermissionDAO.get_by_id(dpt_permission.permission_id).object_type
                    for dpt_permission
                    in DepartmentPermissionDAO.get_all()
                ]))
                func(*args, **kwargs, objects_allowed=objects_allowed)
            if func.__name__ == 'crud_menu':
                crud_actions_allowed = list(dict.fromkeys([
                    permission.crud_action
                    for permission
                    in [PermissionDAO.get_by_id(dpt_permission.permission_id) for dpt_permission in department_permissions]
                    if permission.object_type == kwargs['obj_type']
                ]))
                func(*args, **kwargs, crud_actions_allowed=crud_actions_allowed)
            if func.__name__ == 'filter_owned':
                func(*args, **kwargs, support_contact_id=employee_id)
            if func.__name__ == 'filter_no_signature':
                func(*args, **kwargs)
            if func.__name__ == 'filter_no_support':
                func(*args, **kwargs)
            if func.__name__ == 'filter_due_amount':
                func(*args, **kwargs)
            elif func.__name__ == ('create' or 'delete'):
                # Verify that the object type creation requested in the function is in the list of types allowed
                if kwargs['obj_type'] in obj_type_allowed:
                    func(*args, **kwargs)
                else:
                    click.echo("not allowed '\n")
            elif func.__name__ == 'update':
                # check if user has permission for that type of object
                if kwargs['obj_type'] in obj_type_allowed:
                    # objects allowed in database
                    objects_allowed = [
                        dpt_perm.permission.object_list
                        for dpt_perm in department_permissions
                        if dpt_perm.permission.crud_action == func.__name__
                    ]
                    object_list_allowed = None

                    # construction of command string to get list of allowed objects
                    # general case (all)
                    match objects_allowed[0]:
                        case 'all':
                            match kwargs['obj_type']:
                                case 'client':
                                    object_list_allowed = ClientDAO.get_all()
                                case 'contract':
                                    object_list_allowed = ContractDAO.get_all()
                                case 'event':
                                    object_list_allowed = EventDAO.get_all()
                    # other cases
                    match objects_allowed[0]:
                        case 'owned':
                            match kwargs['obj_type']:
                                case 'client':
                                    object_list_allowed = ClientDAO.filter_by_attr(commercial_id=employee_id)
                                case 'contract':
                                    object_list_allowed = ContractDAO.filter_by_client_commercial_id(employee_id)
                                case 'event':
                                    object_list_allowed = EventDAO.filter_owned(support_contact_id=employee_id)

                    # check if the object included in the attributes is included in the allowed_list
                    if kwargs['obj'] in object_list_allowed:
                        # fields allowed in database
                        fields_allowed = [
                            dpt_perm.permission.object_field
                            for dpt_perm in department_permissions
                            if (dpt_perm.permission.crud_action == func.__name__
                               and dpt_perm.permission.object_type == kwargs['obj_type'])
                        ]
                        if fields_allowed[0] == 'all':
                            fields_allowed = None
                        func(*args, **kwargs, obj_fields_allowed=fields_allowed)
                    else:
                        click.echo("Not allowed \n")
    return wrapper