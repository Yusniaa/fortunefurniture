from odoo import http, fields, models
from odoo.http import request
import json


class KursiCon(http.Controller):
    @http.route(['/kursi','/kursi/<int:idnya>'], auth='public', methods=['GET'], csrf=True)
    def getKursi(self, idnya=None, **kwargs):
        value = []
        if not idnya:
            kursi = request.env['furniture.kursi'].search([])            
            for k in kursi:
                value.append({"id": k.id,
                            "namakursi" : k.name,
                            "stok_tersedia" : k.stok,
                            "harga_sewa" : k.harga,
                            "deskripsi" : k.deskripsi})
            return json.dumps(value)
        else:
            kursiid = request.env['furniture.kursi'].search([('id','=',idnya)])
            for k in kursiid:
                value.append({"id": k.id,
                            "namakursi" : k.name,
                            "stok_tersedia" : k.stok,
                            "harga_sewa" : k.harga,
                            "deskripsi" : k.deskripsi})
            return json.dumps(value)
    
    @http.route('/createkursi',auth='user', type='json', methods=['POST'])
    def createKursi(self, **kw):    
        if request.jsonrequest:    
            if kw['name']:
                vals={
                    'name': kw['name'], 
                    'stok' : kw['stok'],
                    'harga' : kw['harga'],
                    'deskripsi' : kw['deskripsi'],
                }
                kursibaru = request.env['furniture.kursi'].create(vals)
                args = {'success': True, 'ID':kursibaru.id}
                return args

