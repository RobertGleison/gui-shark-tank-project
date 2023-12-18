import logging
from app import APP
import db

'''Cria o servidor onde roda a aplicação. Está rodando na porta 9001, mas vocẽs podem mudar para qualquer porta, como 8080 ou 9000
Sempre que modificarem o código e quiserem testar, devem reiniciar o server.py, mas a porta de escoolherem deve estar vazia.
Se a aplicação voltar um erro dizendo que a porta já está sendo usada, deve liberar a conexão da porta manualmente como os comandos abaixo:

Funciona apenas em terminais linux: 
lsof -i :9001 (ou o seu número da porta) - vai te mostrar o número do processo que está conectado à porta PID
kill -9 PID (coloque o número do processo na palavra PID e pronto, pode rodar o server.py de novo)
'''
if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
  db.connect()
  APP.run(host='0.0.0.0', port=9001)

