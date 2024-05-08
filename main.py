import os
import subprocess
import sys
import time

from markdown import Markdown
from measures_table import MeasuresTable
from model import Model


class Main:

    @staticmethod
    def ask_function():
        return int(input(f'\nEscolha a função:'
                         f'\n1. Gerar documentação de modelo de dados'
                         f'\n2. Exportar tabela com medidas'
                         f'\nEscolha: '))

    @staticmethod
    def ask_model_type():
        return int(input(f'\nEscolha o tipo de modelo de dados:'
                         f'\n1. Modelo de dados pbip'
                         f'\n2. Arquivo model.bim'
                         f'\nEscolha: '))

    @staticmethod
    def ask_ia_description():
        return int(input('\nDeseja gerar interpretações com IA (beta)?'
                         '\n0. Não'
                         '\n1. Somente medidas'
                         '\n2. Somente colunas calculadas'
                         '\n3. Tudo'
                         '\nEscolha: '))

    @staticmethod
    def ask_openai_key():
        return input('\nDigite a chave da API do OpenAI: ')

    @staticmethod
    def ask_measures_table_type():
        return int(input('\nEscolha o tipo de tabela de medidas:'
                         '\n1. Arquivo xlsx'
                         '\n2. Arquivo csv'
                         '\nEscolha: '))

    @staticmethod
    def open_result_folder(path):
        try:
            subprocess.Popen(f'explorer "{path}"')
        except:
            pass

    @staticmethod
    def print_title():
        print("  ____   ____  ___    ")
        print(" |  _ \\ | __ )|_ _|   ")
        print(" | |_) ||  _ \\ | |    ")
        print(" |  __/ | |_) || |    ")
        print(" |_|    |____/|___|   ")
        print("  ____     _   _____   _           __  __   ___   ____   _____  _      ")
        print(" |  _ \\   / \\ |_   _| / \\         |  \\/  | / _ \\ |  _ \\ | ____|| |     ")
        print(" | | | | / _ \\  | |  / _ \\  _____ | |\\/| || | | || | | ||  _|  | |     ")
        print(" | |_| |/ ___ \\ | | / ___ \\|_____|| |  | || |_| || |_| || |___ | |___  ")
        print(" |____//_/   \\_\\|_|/_/   \\_\\      |_|  |_| \\___/ |____/ |_____||_____| ")
        print("  ____    ___    ____      _____  ___    ___   _             ")
        print(" |  _ \\  / _ \\  / ___|    |_   _|/ _ \\  / _ \\ | |            ")
        print(" | | | || | | || |    _____ | | | | | || | | || |            ")
        print(" | |_| || |_| || |___|_____|| | | |_| || |_| || |___         ")
        print(" |____/  \\___/  \\____|      |_|  \\___/  \\___/ |_____|        ")

    def main(self):
        '''
        Main function to generate the documentation of the data model.
        It is executed when the script is called without arguments.
        '''

        function = self.ask_function()

        model = None
        while model is None:
            model_type = self.ask_model_type()
            try:
                if model_type == 1:
                    path = input('\nDigite o caminho da pasta raiz do modelo de dados: ')
                    model = Model(path, model_type=1)
                elif model_type == 2:
                    path = input('\nDigite o caminho da pasta em que está o arquivo model.bim: ')
                    model = Model(path, model_type=2)
            except FileNotFoundError:
                print('\nArquivo não encontrado. Verifique o caminho e tente novamente.')

        if function == 1:
            ia_description = self.ask_ia_description()
            openai_key = self.ask_openai_key() if ia_description != 0 else None
            markdown = Markdown(model, ia_description, openai_key)
            documentacao_md = markdown.gerar_md()
            markdown.salvar_md(documentacao_md)
        elif function == 2:
            measures_table_type = self.ask_measures_table_type()
            if measures_table_type == 1:
                measures_table = MeasuresTable(model)
                measures_table.save_xlsx()
            elif measures_table_type == 2:
                measures_table = MeasuresTable(model)
                measures_table.save_csv()

        self.open_result_folder(path)

    def autorun(self):
        '''
        Function to be executed when the script is called with the argument 'autorun'.
        '''
        path = os.path.dirname(__file__)
        time.sleep(2)
        try:
            model = Model(path, model_type=2)
            markdown = Markdown(model)
            documentacao_md = markdown.gerar_md()
            markdown.salvar_md(documentacao_md)
            time.sleep(5)
            exit()
        except FileNotFoundError:
            print('\nERRO: Nenhum arquivo model.bim foi encontrado na pasta do script.')
            time.sleep(60)


if __name__ == '__main__':
    self = Main()
    self.print_title()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'autorun':
            self.autorun()
    else:
        self.main()
