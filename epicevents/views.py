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

