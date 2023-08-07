import getpass

from InquirerPy import prompt, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator


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
            message="Select an action:",
            choices=choices,
            default=None,
        ).execute()

        return action

    def prompt_for_client_creation(self):
        first_name = inquirer.text(message="Saisir prénom du client:").execute()
        last_name = inquirer.text(message="Saisir nom du client:").execute()
        email = inquirer.text(message="Saisir email du client:").execute()
        telephone = inquirer.text(message="Saisir numéro de téléphone du client:").execute()
        company_name = inquirer.text(message="Saisir nom de l'entreprise du client:").execute()
        commercial_id = inquirer.text(message="Saisir id du commercial responsable:").execute()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "telephone": telephone,
            "company_name": company_name,
            "commercial_id": commercial_id,
        }



