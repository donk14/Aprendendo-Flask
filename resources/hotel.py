from flask_restful import Resource, reqparse
from models.hotel import HotelModel
#Pra conseguir receber os elementos JSON da nossa requisição vamos precisar do reqparse
#JSON = JavaScript Object Notation é um formato leve para trocas de informações/dados
hoteis = [
        {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
        },
        {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
        },
        {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Belém'
        }
]

class Hoteis(Resource):
    def get(self):
        return{'hoteis': hoteis}

class Hotel(Resource):
    #Como iam ser usados em mais de uma função, resolveu-se deixá-los como atributos da classe
    argumentos = reqparse.RequestParser()
    #Só vai aceitar os argumentos que estão definido aqui:
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                    return hotel
        return None

    def get(self, hotel_id):
        #pass #Serve pra gente não implementar por agora e depois poderá assim fazê-lo.
        hotel = Hotel.find_hotel(hotel_id)
        if hotel: #se existe hotel_id
            return hotel
        return{'message': 'Hotel não encontrado'}, 404 #HTTP not found

    def post(self, hotel_id):
        #criar um construtor com todos os argumentos adicionados
        #"dados" será chave e valor de todos os argumentos passados.
        dados = Hotel.argumentos.parse_args()
        #Vamos construir nosso Novo Hotel que será um JSON
        #Esses dados lá de cima vão como um dicionário.

        #novo_hotel = {
        #    'hotel_id': hotel_id,
        #    'nome': dados['nome'],
        #    'estrelas': dados['estrelas'],
        #    'diaria': dados['diaria'],
        #    'cidade': dados['cidade']
        #}
        #nomo_hotel é um objeto
        hotel_objeto = HotelModel(hotel_id, **dados)
        #novo_hotel = {'hotel_id': hotel_id, **dados}
        #Dessa forma será convertido em dicionário e depois em json
        novo_hotel = hotel_objeto.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 200 #Ok

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        #**dados vai desembrulhar e já vai criar a chave e o valor para cada item de dados, como feitos anteriormente
        #novo_hotel = {'hotel_id': hotel_id, **dados}
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200 # ok
        else:
            hoteis.append(novo_hotel)
            return novo_hotel, 201 #Criado com Sucesso

    def delete(self, hotel_id):
        #Assim o Python entende que a variável hoteis é a que foi referenciada lá em cima
        global hoteis
        #Vamos criar uma nova lista retirando o id do hotel que foi passado como parâmetro
        #Eu quero que retorne hotel para cada hotel dento de Hoteis
        #Com a condição, se o hotel com id em questão não for igual o id do hotel passado
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return{'message': 'Hotel Deleted'}

#CRUD finalizado com sucesso (Create, Read, Update and Delete)
