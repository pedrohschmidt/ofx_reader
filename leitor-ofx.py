import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
from ofxparse import OfxParser, OfxParserException
import csv

def find_ofx_files(directory):

    ofx_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ofx'):
                #print(file)
                ofx_files.append(os.path.join(root, file))
    return ofx_files

def read_ofx_files(ofx_files):

    ofx_data = []
    for file in ofx_files:
        try:
            with open(file, 'r', errors='ignore', encoding='latin-1') as f:
                ofx = OfxParser.parse(f)
                ofx_data.append((file, ofx))
        except OfxParserException as e:
            print(f"Error parsing {file}: {e}")
        except UnicodeDecodeError as e:
            print(f"Error decoding {file}: {e}")
    return ofx_data

def main():
    # Cria uma janela Tkinter oculta
    root = Tk()
    root.withdraw()

    # Colocar o destino onde o arquivo com o resumo deve ser salvo:
    caminho_destino = "C:\\Users\\pschmidt\\Desktop\\teste ofx\\"
    # Abre a janela de seleção de diretório
    directory_path = askdirectory(title='Selecione o diretório onde buscar os arquivos OFX')
    #directory_path = "C:\\Users\\pschmidt\\Desktop\\teste ofx"
    # Verifica se o usuário selecionou um diretório
    if directory_path:
        # Encontrar todos os arquivos OFX na pasta e suas subpastas
        ofx_files = find_ofx_files(directory_path)
        # Ler e processar os arquivos OFX encontrados
        ofx_data = read_ofx_files(ofx_files)

        output_file = os.path.join(caminho_destino, 'ofx_info.csv')
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Arquivo', 'Conta', 'Agência', 'Início OFX', 'Final OFX', 'contagem_creditos', 'total_creditos', 'contagem_debitos', 'total_debitos', 'Balance OFX' ])
        
            # Exemplo de como acessar os dados lidos
            for file, ofx in ofx_data:
                print(f"Arquivo: {file}")
                for account in ofx.accounts:
                    statement = account.statement
                    total_credit = 0
                    total_debit= 0
                    credit_count = 0
                    debit_count = 0
                    for transaction in account.statement.transactions:
                        if transaction.amount > 0:
                            credit_count += 1
                            total_credit += transaction.amount
                        elif transaction.amount < 0:
                            debit_count += 1
                            total_debit += transaction.amount

                    csvwriter.writerow([file, account.account_id, account.branch_id, statement.start_date, statement.end_date, credit_count, total_credit, debit_count, total_debit, statement.balance ])


                    #for transaction in account.statement.transactions:
                    #    print(f"Transação: {transaction.date} - {transaction.amount} - {transaction.memo}")
        print('Processamento finalizado')            
    else:
        print("Nenhum diretório selecionado.")

if __name__ == '__main__':
    main()
