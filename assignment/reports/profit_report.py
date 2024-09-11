from odoo import models, fields, api

class ProfitReport(models.AbstractModel):
    _name = 'report.custom_addons.profit_report'
    _description = 'Profit Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'docs': self.env['product.product'].browse(docids),
        }
