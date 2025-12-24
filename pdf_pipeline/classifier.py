import re

purchase_category_dict = {
      'Shopping e ecommerce': {
          'Mercadolivre', 'Livraria', 'Mp', 'Mlp', 'Americanas', 'Pdv', 'So Ler',
          'Pag', 'Hna', 'Amazon', 'Renner', 'Zara', 'Acessorios', 'Melissa',
          'Shopee', 'Lolja', 'Saoleopoldomeias', 'Marisa', 'Prata', 'Moda',
          'Bazar', 'Brecho', 'Shopping', 'Magalu', 'Shein', 'Torra Torra', 'Marbela', 'Festa', 'Presente', 'Armarinhos'
      },
      'Ifood': {
          'ifd', 'ifood'
      },
      'Restaurantes': {
          'The Waffle King', 'Coffee', 'Divino Fogao', 'Pub', 'Restaurante',
          'Ceu da Boca', 'Bar', 'Cafe', 'Bistr', 'Ru Unisinos', 'Bocattino',
          'Mokai', 'Mercearia', 'Pampa', 'Sorveteria', 'Mood', 'Cantina',
          'Ice Cream'
      },
      'Lanches e Conveniencias': {
          'Station', 'Posto', 'Lanche', 'Happy Station', 'Florinda',
          'Conveniencias'
      },
      'Mercados': {
          'Macromix', 'Padaria', 'Supermercado', 'Bourbon', 'Atacado',
          'Mercado', 'Havan', 'Zaffari', 'Unidasul', 'Frutas', 'Minimercado',
          'Casa dos Cereais', 'Armazem 88'
      },
      'Shows e cinema': {
          'Tickets', 'Cinema', 'Opiniao', 'Sympla'
      },
      'Transporte': {
          'Palmares', 'Uber*', 'Uber', 'Citral', 'Via Sul'
      },
      'Saude e Farmacia': {
          'Pharma', 'Odonto', 'Farmacia', 'Atendvip', 'Oi Digital',
          'Panvel', 'Farma', 'Gabriel', 'Betterme'
      },
      'Beleza': {
          'Opus', 'Miriammf', 'Boticario', 'Beleza'
      },
      'Lavanderia': {
          'Cicclo', 'Begin'
      },
      'Assinaturas e Servicos': {
          'Prime', 'Tembici', 'Netflix', 'Spotify', 'Vogue'
      },
      'Casa': {
          'Imobiliaria', 'Net', 'Rge', 'Claro', 'Flex'
      },
      'Faculdade': {
          'Matricula', 'Unisinos'
      },
      'Apostas': {
          'Sorte'
      },
      'Bar': {
          'Brecho do Futebol', 'Majestic', 'Quiosque', 'Drink'
      },
      'Tecnologia e Projetos': {
          'Openai'
      },
      'Viagem': {
          'Airbnb'
      }
}

def classify_purchases(purchase_description):
    for category, keywords in purchase_category_dict.items():
        for keyword in keywords:
            if keyword.lower() in purchase_description.lower():
                return category
    return 'Outro'