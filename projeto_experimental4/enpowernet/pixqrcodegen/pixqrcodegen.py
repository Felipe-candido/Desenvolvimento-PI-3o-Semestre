import crcmod
import qrcode
import os

class Payload():
    def __init__(self, nome, chavepix, valor, cidade ,txtId):

        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor
        self.cidade = cidade
        self.txtId = txtId

        self.tam_nome = len(self.nome)
        self.tam_chavepix = len(self.chavepix)
        self.tam_valor = len(self.valor)
        self.tam_cidade = len(self.cidade) 
        self.tam_txtId = len(self.txtId)    

        self.tam_merchantAccount = f'0014BR.GOV.BCB.PIX01{self.tam_chavepix}{self.chavepix}'

        self.payloadFormat = '000201'

        self.merchantAccount = f'26{len(self.tam_merchantAccount)}{self.tam_merchantAccount}'

        if self.tam_valor <=9:
            self.tam_transactionAmount = f'0{self.tam_valor}{self.valor}'
        else:
             self.tam_transactionAmount = f'{self.tam_valor}{self.valor}'

        if self.tam_txtId <=9:
            self.tam_addDataField = f'050{self.tam_txtId}{self.txtId}'
        else:
             self.tam_addDataField = f'05{self.tam_txtId}{self.txtId}'

        if self.tam_nome <=9:
            self.tam_nome = f'0{self.tam_nome}'

        if self.tam_cidade <=9:
            self.tam_cidade = f'0{self.tam_cidade}'


        self.merchantCategCode = '52040000'
        self.transactionCurrency = '5303986'
        self.transactionAmount = f'54{self.tam_transactionAmount}'
        self.countryCode = '5802BR'
        self.merchantName = f'59{self.tam_nome}{self.nome}'
        self.merchantCity = f'60{self.tam_cidade}{self.cidade}'
        self.addDataField = f'62{len(self.tam_addDataField)}{self.tam_addDataField}'
        self.crc16 = '6304'

    def PayloadGen(self):
        self.payload = f'{self.payloadFormat}{self.merchantAccount}{self.merchantCategCode}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}'

        print()
        print(self.payload)
        print()

        self.crc16gen(self.payload)


    def crc16gen(self, payload):
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF,rev=False, xorOut=0x0000)
    
        self.crc16Code = hex(crc16(str(payload).encode('utf-8')))

        

        self.crc16_format = str(self.crc16Code).replace('0x', '').upper()

        self.payload_retorno = f'{payload}{self.crc16_format}'

        
        print(self.payload_retorno)

        self.qrcodegen(self.payload_retorno)

    def qrcodegen(self, payload):
        self.qrcode = qrcode.make(payload)
        
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        os.makedirs(static_dir, exist_ok=True)  
        

        qrcode_path = os.path.join(static_dir, 'pixqrcode.png')
        self.qrcode.save(qrcode_path)

if __name__ == '__main__':
    p = Payload('Darlan dos santos', 'darlanj207@gmail.com', '422.00', 'Araras', 'Cidade02')
    p.PayloadGen()
