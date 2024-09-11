from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    scheduled_date = fields.Date(string='Scheduled Date')

    # product_ids_received = fields.Many2many('product.product', 'sale_order_product_received_rel', 'order_id', 'product_id', string="Products Received")
    payment_ids = fields.One2many('account.payment', 'sale_order_id', string='Payments')
    payments_made = fields.Monetary(compute='_compute_payments_made', string='Payments Made',
                                    currency_field='currency_id')

    @api.depends('payment_ids')
    def _compute_payments_made(self):
        for order in self:
            order.payments_made = sum(payment.amount for payment in order.payment_ids)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Profit margin field
    cost_price = fields.Float(string="Cost Price")
    selling_price = fields.Float(string="Selling Price")

    @api.depends('cost_price', 'selling_price')
    def _compute_profit_margin(self):
        for product in self:
            if product.cost_price:
                product.profit_margin = (product.selling_price - product.cost_price) / product.cost_price * 100
            else:
                product.profit_margin = 0.0

    profit_margin = fields.Float(string="Profit Margin", compute='_compute_profit_margin')

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
