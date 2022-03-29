from odoo import api, fields, models

class Meja(models.Model):
    _name = 'furniture.meja'
    _description = 'Meja'

    name = fields.Char(string='Nama')
    stok = fields.Integer(string='Stok')
    harga = fields.Integer(string='Harga')
    deskripsi = fields.Char(string='Deskripsi')