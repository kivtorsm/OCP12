import getpass

from InquirerPy import prompt, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from models import Client, Contract, Event, Employee

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
}


class ClientView:
    def prompt_for_main_menu(self):
        choices = [
            Choice('client', name="Clients"),
            Choice('contract', name="Contrats"),
            Choice('event', name="Evènements"),
            Choice('employee', name="Collaborateurs"),
            Separator(),
            Choice('exit', name="Menu principal"),
        ]
        action = inquirer.select(
            message="Choisissez un menu:",
            choices=choices,
            default=None,
        ).execute()
        print("")

        return action

    def prompt_for_crud_menu(self, obj_type: str):

        choices = [
            Choice('create', name=f"Créer un {NAMES[obj_type]}"),
            Choice('show_all', name=f"Consulter la liste des {NAMES[obj_type]}s"),
            Choice('show_details', name=f"Consulter les détails d'un {NAMES[obj_type]}"),
            Choice('update', name=f"Modifier {NAMES[obj_type]}"),
            Choice('delete', name=f"Supprimer un {NAMES[obj_type]}"),
            Separator(),
            Choice('exit', name="Fermer application"),
        ]

        action = inquirer.select(
            message="Sélectionner une action:",
            choices=choices,
            default=None,
        ).execute()
        print("")

        return action

    def prompt_for_client_creation(self):
        first_name = inquirer.text(message="Saisir prénom du client:").execute()
        last_name = inquirer.text(message="Saisir nom du client:").execute()
        email = inquirer.text(message="Saisir email du client:").execute()
        telephone = inquirer.text(message="Saisir numéro de téléphone du client:").execute()
        company_name = inquirer.text(message="Saisir nom de l'entreprise du client:").execute()
        commercial_id = inquirer.text(message="Saisir id du commercial responsable:").execute()
        print("")
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "telephone": telephone,
            "company_name": company_name,
            "commercial_id": commercial_id,
        }

    def show_obj_list(self, obj_list: list):
        [print(obj) for obj in obj_list]
        print("")

    def show_details(self, obj: object):
        print(obj)
        print("")

    def prompt_for_object_id(self, action: str, obj_type: str):

        obj_id = inquirer.text(message=f"Saisir id du {NAMES[obj_type]} à {ACTIONS[action]}:").execute()
        print("")
        return obj_id

    def prompt_for_object_field_update(self, client: Client):
        fields_excluded = [
            "_sa_instance_state",
            "created",
            "id",
            "modified",
        ]
        field_choices = [Choice(attr, name=f"{attr}: {value}") for attr, value in client.__dict__.items() if attr not in fields_excluded]
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
                print(obj)
                print("")
            case 'update':
                print(f"Le {obj_type} a été correctement modifié")
                print(obj)
                print("")
            case 'delete':
                print(f"Le {obj_type} a été correctement supprimé")
                print("Enregistrement supprimé :")
                print(obj)
                print("")
