import pandas as pd
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#Vamos ler as duas bases de dados
base_vendas = pd.read_csv("VagaDev/vendas.csv")
base_leads = pd.read_csv("VagaDev/leads.csv")
#Vamos deixar as colunas alinhadas
base_vendas.columns = ['Unnamed: 0', 'cod_nf', 'cod_prod', 'cpf', 'email', 'telefone', 'valor', 'quantidade']
cpf = base_vendas['cpf']
#Vamos ver só os que tem nos dois df
together_inner = pd.merge(base_leads, base_vendas).to_json()
#together_inner = base_vendas.merge(base_leads, on=[''])
#print(together_inner)

class Vendas_Concretizadas(Resource):
    def get(self):
        return{'Vendas_Concretizadas': together_inner}

class Venda(Resource):
    def get(self, cpf):
        #pass #Serve pra gente não implementar por agora e depois poderá assim fazê-lo.
        for venda in together_inner:
            if venda['cpf'] == cpf:
                    return venda
        return{'message': 'Venda não encontrada'}, 404 #HTTP not found

api.add_resource(Vendas_Concretizadas, '/vendas_concretizadas')
api.add_resource(Venda, '/vendas_concretizadas/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True)
