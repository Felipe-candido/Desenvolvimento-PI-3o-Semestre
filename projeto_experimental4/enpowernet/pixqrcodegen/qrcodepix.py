import qrcode
from pixqrcodegen import Payload

def payload_to_qr_code(nome, chavepix, valor, cidade, txtId):
    
    payload_obj = Payload(nome, chavepix, valor, cidade, txtId)
    payload = payload_obj.PayloadGen()  

    
    QR = qrcode.make(payload)
    QR.save('pixqrcode.png')

if __name__ == '__main__':
    
    payload_to_qr_code('Bruno gay', 'bruno69@gmail.com', '500.00', 'Leme', 'Cidade de traveco69')
