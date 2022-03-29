from odoo import api, fields, models

class SetMejaKursi(models.Model):
    _name = 'furniture.setmejakursi'
    _description = 'Set Meja dan Kursi'

    name = fields.Char(string='Nama Paket')
    meja_id = fields.Many2one(comodel_name='furniture.meja', string='Meja', required=True)
    kursi_id = fields.Many2one(comodel_name='furniture.kursi', string='Kursi', required=True)
    stok = fields.Integer(string='Stok')
    harga = fields.Integer(compute = '_compute_harga',string='Harga')
    diskon = fields.Integer(string='Diskon')
    

    @api.depends('meja_id', 'kursi_id', 'diskon')
    def _compute_harga(self):
        for record in self:
            record.harga = (record.meja_id.harga + record.kursi_id.harga) - record.diskon