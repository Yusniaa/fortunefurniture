from odoo import api, fields, models


class Pengiriman(models.Model):
    _name = 'furniture.pengiriman'
    _description = 'Pengiriman Barang Sewa'

    name = fields.Char(compute='_compute_nama_penyewa', string='Nama Penyewa')
    order_id = fields.Many2one(comodel_name='furniture.order', string='No. Order')
    
    @api.depends('order_id')
    def _compute_nama_penyewa(self):
        for record in self:
            record.name = self.env['furniture.order'].search([('id', '=', record.order_id.id)]).mapped('pemesan').name
    
    tgl_pengiriman = fields.Date(string='Tanggal pengiriman', default=fields.Date.today())
    
    tagihan = fields.Integer(compute='_compute_tagihan', string='Tagihan')
    
    @api.depends('order_id')
    def _compute_tagihan(self):
        for record in self:
            record.tagihan = record.order_id.total            
   
        
    @api.model
    def create(self,vals):
        record = super(Pengiriman, self).create(vals) 
        if record.tgl_pengiriman:
            self.env['furniture.order'].search([('id','=',record.order_id.id)]).write({'sudah_kirim':True}) 
            self.env['furniture.akunting'].create({'kredit' : record.tagihan, 'name':record.name})          
            return record

    def unlink(self):
        for x in self:
            self.env['furniture.order'].search([('id','=',x.order_id.id)]).write({'sudah_kirim':False})
        record = super(Pengiriman, self).unlink()
   