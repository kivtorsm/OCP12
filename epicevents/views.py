import getpass
import click

from typing import Tuple, Union

from rich.panel import Panel
from rich import box

from InquirerPy import prompt, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from models import Client, Contract, Event, Employee
from display import Display


NAMES = {
            'client': "client",
            'contract': "contrat",
            'event': "évènement",
            'employee': "employé",
        }

ACTIONS = {
    'show': "consulter",
    'update': "mettre à jour",
    'delete': "supprimer",
    'create': "créer",
}


EXCLUDED_FIELDS = [
            "_sa_instance_state",
            "created",
            "id",
            "modified",
            "commercial_id",
            "support_contact_id",
        ]

FIELDS = {
    'first_name': "prénom",
    'last_name': "nom",
    'email': "e-mail",
    'telephone': "téléphone",
    'company_name': "entreprise",
    'commercial_id': "ID du commercial",
    'client_id': "ID du client",
    'total_amount': "Montant total",
    'due_amount': "Montant restantà payer",
    'status': "Etat",
    'contract_id': "ID du contrat",
    'start_date': "Date de début",
    'end_date': "Date de fin",
    'support_contact_id': "ID contact support",
    'location': "Lieu",
    'attendees_number': "Nombre de participants",
    'notes': "Notes",
    'department_id': "ID du département",
    'encoded_hash': "Mot de passe",

}

class CrudView:
    @staticmethod
    def prompt_for_main_menu(allowed_objects: list = None):
        choices = [
            obj for obj in allowed_objects if obj is not None
        ]
        obj_choices = [Choice(obj, name=f"{NAMES[obj].capitalize()}s") for obj in choices]
        obj_choices.append(Separator())
        obj_choices.append(Choice('exit', name="Fermer application"))

        action = inquirer.select(
            message="Choisissez un menu:",
            choices=obj_choices,
            default=None,
        ).execute()
        print("")

        return action

    @staticmethod
    def prompt_for_crud_menu(obj_type: str, crud_actions_allowed: list = None):
        ACTIONS_LONG = {
            'show': f"consulter tous les {NAMES[obj_type]}s",
            'show_details': f"consulter les détails d'un {NAMES[obj_type]}",
            'update': f"mettre à jour un {NAMES[obj_type]}",
            'delete': f"supprimer un {NAMES[obj_type]}",
            'create': f"créer un {NAMES[obj_type]}",
        }
        choices = [
            action for action in crud_actions_allowed if action is not None
        ]
        crud_choices = [
            Choice('show_all', name=f"Consulter la liste des {NAMES[obj_type]}s"),
            Choice('show_details', name=f"Consulter les détails d'un {NAMES[obj_type]}"),
        ]
        for action in choices:
            crud_choices.append(
                Choice(action, name=f"{ACTIONS_LONG[action].capitalize()}")
            )
        crud_choices.append(Separator())
        crud_choices.append(Choice('exit', name="Menu principal"))

        action = inquirer.select(
            message="Sélectionner une action:",
            choices=crud_choices,
            default=None,
        ).execute()

        print("")

        return action

    @staticmethod
    def prompt_for_object_creation(obj_type: str):
        print(f"Saisissez les données du {NAMES[obj_type]}:")
        obj_data = {}
        attr_list = []
        match obj_type:
            case 'client':
                attr_list = Client.__table__.columns
            case 'contract':
                attr_list = Contract.__table__.columns
            case 'event':
                attr_list = Event.__table__.columns
            case 'employee':
                attr_list = Employee.__table__.columns
        short_attr_list = [str(attr).replace(f"{obj_type}.", "") for attr in attr_list]
        for attr in short_attr_list:
            if attr not in EXCLUDED_FIELDS:
                obj_data[attr] = inquirer.text(message=f"{FIELDS[attr]}").execute()
        print("")
        return obj_data

    @staticmethod
    def show_obj_list(obj_list: list):
        [print(obj) for obj in obj_list]
        print("")

    @staticmethod
    def show_details(obj: object):
        print(obj)
        print("")

    @staticmethod
    def prompt_for_object_id(action: str, obj_type: str):

        obj_id = inquirer.text(message=f"Saisir id du {NAMES[obj_type]} à {ACTIONS[action]}:").execute()
        print("")
        return obj_id

    @staticmethod
    def prompt_for_object_field_update(obj: object, allowed_fields: list = None) -> (str, str):
        allowed_fields = allowed_fields if allowed_fields else [
            attr
            for attr, value
            in obj.__dict__.items()
        ]

        field_choices = [
            Choice(attr, name=f"{attr}: {value}")
            for attr, value
            in obj.__dict__.items()
            if (attr in allowed_fields and attr not in EXCLUDED_FIELDS)
        ]
        field_to_modify = inquirer.select(
            message="Sélectionner un champ à modifier:",
            choices=field_choices,
            default=None,
        ).execute()
        print("")

        new_value = inquirer.text(message=f"Saisir nouvelle valeur pour {field_to_modify}:").execute()
        print("")
        return field_to_modify, new_value

    @staticmethod
    def prompt_for_confirmation(change: str, obj_type: str, obj: object):
        match change:
            case 'create':
                print(f"Le {NAMES[obj_type]} a été correctement créé")
            case 'update':
                print(f"Le {obj_type} a été correctement modifié")
            case 'delete':
                print(f"Le {obj_type} a été correctement supprimé")
                print("Enregistrement supprimé :")

        print(obj)
        print("")


class LoginView:
    def __init__(self):
        self.display = Display()

    def prompt_login_details(self) -> Tuple[str, str]:

        self.display.log(
            "Saisissez votre email et votre mot de passe et tapez entrée, ou appuyez sur ctrl+c pour sortir : "
        )
        email = getpass.getpass(prompt="Email :")
        password = getpass.getpass(prompt="Mot de passe :")
        return email, password

    def succesful_login(self):
        click.echo("Vous êtes bien connectés")

    def already_logged_in(self):
        click.echo(
            "Vous êtes déjà connectés ! \nEssayez --relogin pour mettre à jour vos informations de connexion!"
        )
