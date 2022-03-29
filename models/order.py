from odoo.exceptions import ValidationError
from odoo import api, fields, models

class Order(models.Model):
    _name = 'furniture.order'
    _description ='Order'

    ordersetmejakursi_ids = fields.One2many(
        comodel_name='furniture.ordersetmejakursi', 
        inverse_name='order_id', 
        string='Order Set Meja dan Kursi')
    
    ordermejadetail_ids = fields.One2many(
        comodel_name='furniture.ordermejadetail', 
        inverse_name='orderm_id', 
        string='Order Meja')

    orderkursidetail_ids = fields.One2many(
        comodel_name='furniture.orderkursidetail', 
        inverse_name='orderk_id', 
        string='Order Kursi')

    orderlemaridetail_ids = fields.One2many(
        comodel_name='furniture.orderlemaridetail', 
        inverse_name='orderl_id', 
        string='Order Lemari')
    
    name = fields.Char(string='Kode Order', required=True)
    tanggal_pesan = fields.Datetime('Tanggal Pemesanan',default=fields.Datetime.now())
    pemesan = fields.Many2one(
        comodel_name='res.partner', 
        string='Pemesan', 
        domain=[('is_customer','=', True)],store=True)
        
    
    total = fields.Integer(compute='_compute_total', string='Total', store=True)
    
    @api.depends('ordersetmejakursi_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['furniture.ordersetmejakursi'].search([('order_id', '=', record.id)]).mapped('harga'))
            b = sum(self.env['furniture.ordermejadetail'].search([('orderm_id', '=', record.id)]).mapped('harga'))
            c = sum(self.env['furniture.orderkursidetail'].search([('orderk_id', '=', record.id)]).mapped('harga'))
            d = sum(self.env['furniture.orderlemaridetail'].search([('orderk_id', '=', record.id)]).mapped('harga'))
            record.total = a + b + c + d

    sudah_kirim= fields.Boolean(string='Sudah Dikirimkan', default=False)

class OrderSetMejaKursi(models.Model):
    _name = 'furniture.ordersetmejakursi'
    _description = 'Order Set Meja dan Kursi'

    order_id = fields.Many2one(comodel_name='furniture.order', string='Order')
    setmejakursi_id = fields.Many2one(comodel_name='furniture.setmejakursi', string='Meja dan Kursi')
    
    name = fields.Char(string='Nama')
    harga = fields.Integer(compute = '_compute_harga',string='Harga')
    qty = fields.Integer(string='Quantity')
    harga_satuan = fields.Integer(compute = '_compute_harga_satuan',string='Harga Satuan')
    
    
    @api.depends('setmejakursi_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.setmejakursi_id.harga

    
    @api.depends('qty', 'harga_satuan')
    def _compute_harga(self):
        for record in self:
            record.harga = record.harga_satuan * record.qty

    @api.model
    def create(self,vals):
        record = super(OrderSetMejaKursi, self).create(vals)
        if record.qty:
            self.env['furniture.setmejakursi'].search([('id', '=',record.setmejakursi_id.id)]).write({'stok':record.setmejakursi_id.stok-record.qty})      
            return record

class OrderMejaDetail(models.Model):
    _name = 'furniture.ordermejadetail'
    _description = 'Order Meja'

    orderm_id = fields.Many2one(comodel_name='furniture.order', string='Order')
    meja_id = fields.Many2one(
        comodel_name='furniture.meja', 
        string='Meja',
        domain=[('stok','>','1')])
        
    name = fields.Char(string='Nama')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan',string='Harga Satuan')
        
        
    @api.depends('meja_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.meja_id.harga

    qty = fields.Integer(string='Quantity')
        
        
    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            a=self.env['furniture.meja'].search([('stok','<', record.qty),('id','=',record.id)])
            if a:
                raise ValidationError("Stok meja yang dipilih tidak cukup")
        
    harga = fields.Integer(compute='_compute_harga',string='Harga')

        
    @api.depends('harga_satuan','qty')
    def _compute_harga(self):
        for record in self:
            record.harga = record.harga_satuan * record.qty

    @api.model
    def create(self,vals):
        record = super(OrderMejaDetail, self).create(vals)
        if record.qty:
            self.env['furniture.meja'].search([('id','=',record.meja_id.id)]).write({'stok':record.meja_id.stok-record.qty})
            return record
        
class OrderKursiDetail(models.Model):
    _name = 'furniture.orderkursidetail'
    _description = 'Order Kursi'

    orderk_id = fields.Many2one(comodel_name='furniture.order', string='Order')
    kursi_id = fields.Many2one(
        comodel_name='furniture.kursi', 
        string='Kursi',
        domain=[('stok','>','1')])
        
    name = fields.Char(string='Nama')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan',string='Harga Satuan')
        
        
    @api.depends('kursi_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.kursi_id.harga

    qty = fields.Integer(string='Quantity')
        
        
    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            a=self.env['furniture.kursi'].search([('stok','<', record.qty),('id','=',record.id)])
            if a:
                raise ValidationError("Stok kursi yang dipilih tidak cukup")
        
    harga = fields.Integer(compute='_compute_harga',string='Harga')

        
    @api.depends('harga_satuan','qty')
    def _compute_harga(self):
        for record in self:
            record.harga = record.harga_satuan * record.qty

    @api.model
    def create(self,vals):
        record = super(OrderKursiDetail, self).create(vals)
        if record.qty:
            self.env['furniture.kursi'].search([('id','=',record.kursi_id.id)]).write({'stok':record.kursi_id.stok-record.qty})
            return record
        
class OrderLemariDetail(models.Model):
    _name = 'furniture.orderlemaridetail'
    _description = 'Order Lemari'

    orderl_id = fields.Many2one(comodel_name='furniture.order', string='Order')
    lemari_id = fields.Many2one(
        comodel_name='furniture.lemari', 
        string='Lemari',
        domain=[('stok','>','1')])
        
    name = fields.Char(string='Nama')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan',string='Harga Satuan')
        
        
    @api.depends('lemari_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.lemari_id.harga

    qty = fields.Integer(string='Quantity')
        
        
    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            a=self.env['furniture.lemari'].search([('stok','<', record.qty),('id','=',record.id)])
            if a:
                raise ValidationError("Stok lemari yang dipilih tidak cukup")
        
    harga = fields.Integer(compute='_compute_harga',string='Harga')

        
    @api.depends('harga_satuan','qty')
    def _compute_harga(self):
        for record in self:
            record.harga = record.harga_satuan * record.qty

    @api.model
    def create(self,vals):
        record = super(OrderLemariDetail, self).create(vals)
        if record.qty:
            self.env['furniture.lemari'].search([('id','=',record.lemari_id.id)]).write({'stok':record.lemari_id.stok-record.qty})
            return record