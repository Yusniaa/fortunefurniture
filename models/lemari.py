from odoo import api, fields, models

class Lemari(models.Model):
    _name = 'furniture.lemari'
    _description = 'Lemari'

    name = fields.Char(string='Nama')
    stok = fields.Integer(string='Stok')
    harga = fields.Integer(string='Harga')
    deskripsi = fields.Char(string='Deskripsi')