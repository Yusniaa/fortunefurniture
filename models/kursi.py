from odoo import api, fields, models

class Kursi(models.Model):
    _name = 'furniture.kursi'
    _description = 'Kursi'

    name = fields.Char(string='Name')
    stok = fields.Integer(string='Stok Kursi')
    harga = fields.Integer(string='Harga')
    deskripsi = fields.Char(string='Deskripsi')
    
    