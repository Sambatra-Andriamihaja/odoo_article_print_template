from odoo import models, fields, api

class ArticlePrintTemplate(models.Model):
    _inherit = "product.template"
    _description = 'Article report'

    price_excl_vat = fields.Float(string="Prix Hors Taxe", compute="_compute_price_excl_vat", store=True)
    discount = fields.Float(string="Remise", compute="_compute_discount", store=True)
    vat = fields.Float(string="TVA", compute="_compute_vat", store=True)
    total_price = fields.Float(string="Prix TTC", compute="_compute_total_price", store=True)
    
    @api.depends('list_price')
    def _compute_price_excl_vat(self):
        for record in self:
            if record.list_price:
                record.price_excl_vat = record.list_price
            else:
                record.price_excl_vat = 0.0
            
    @api.depends('price_excl_vat')
    def _compute_discount(self):
        # For now, the discount rate is 0% (remise 0%)
        discount_rate = 0.0
        for record in self:
            record.discount = record.price_excl_vat * discount_rate
        
    @api.depends('price_excl_vat')
    def _compute_vat(self):
        # VAT rate 20% (TVA 20%)
        vat_rate = 0.20
        for record in self:
            record.vat = record.price_excl_vat * vat_rate
        
    @api.depends('price_excl_vat', 'discount', 'vat')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.price_excl_vat - record.discount + record.vat

    