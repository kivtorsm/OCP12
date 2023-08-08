import getpass

from InquirerPy import prompt, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from models import Client


class ClientView:
    def prompt_for_client_crud_menu(self):
        choices = [
            Choice('create_client', name="Créer client"),
            Choice('show_all_clients', name="Consulter la liste des clients"),
            Choice('show_client_detail', name="Consulter les détails d'un client"),
            Choice('update_client', name="Modifier client"),
            Choice('delete_client', name="Supprimer un client"),
            Separator(),
            Choice('exit', name="Sortir"),
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

    def show_client_list(self, clients: list):
        [print(client) for client in clients]
        print("")

    def show_client_details(self, client: Client):
        print(client)
        print("")

    def prompt_for_client_id(self, action: str):
        actions = {
            'show': "consulter",
            'update': "mettre à jour",
            'delete': "supprimer",
        }
        client_id = inquirer.text(message=f"Saisir id du client à {actions[action]}:").execute()
        print("")
        return client_id

    def prompt_for_client_field_update(self, client: Client):
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
