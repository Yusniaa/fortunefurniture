from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    is_pegawai = fields.Boolean(string='Pegawai')
    is_customer = fields.Boolean(string='')
    
    