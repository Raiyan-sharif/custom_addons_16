from odoo import api, fields, models
from datetime import datetime

class Assignment2Invoice(models.Model):
    _name = 'assignment2.invoice'
    _description = 'Assignment2 Invoice'

    invoicing_address = fields.Char(string="Invoicing Address", required=True)
    invoice_number = fields.Char(string="Invoice Number", required=True, default=lambda self: self._generate_invoice_number())
    decision_number = fields.Char(string="Decision Number")
    invoice_date = fields.Date(string="Invoice Date", default=fields.Date.context_today, required=True)
    date_of_decision = fields.Date(string="Date of Decision")
    due_date = fields.Date(string="Due Date")
    tax_type = fields.Selection([('vat', 'VAT'), ('gst', 'GST'), ('sales', 'Sales Tax')], string="Tax Type", required=True)
    declaration = fields.Text(string="Declaration")
    amount_total = fields.Monetary(string="Total Amount Payable", currency_field='currency_id', required=True)
    recipient_account_number = fields.Char(string="Recipient's Account Number", required=True)
    recipient_name = fields.Char(string="Recipient's Name", required=True)
    payer_name = fields.Many2one('hr.employee', string="Payer's Name", required=True)  # Changed to employee reference
    payer_address = fields.Char(string="Payer's Address", required=True)
    signature = fields.Binary(string="Signature")
    from_account_no = fields.Char(string="From Account Number", required=True)
    bic = fields.Char(string="BIC", required=True)
    barcode_field = fields.Char(string="Virtual Barcode", compute='_generate_barcode')
    reference_number = fields.Char(string="Reference Number")
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)

    currency_id = fields.Many2one('res.currency', string="Currency")

    # Methods to generate invoice number and barcode
    @api.model
    def _generate_invoice_number(self):
        year_month = datetime.today().strftime('%Y%m')
        sequence = self.env['ir.sequence'].next_by_code('assignment2.invoice') or '001'
        return f'{year_month}{sequence}'

    @api.depends('invoice_number')
    def _generate_barcode(self):
        for invoice in self:
            invoice.barcode_field = f'V5-{invoice.invoice_number}'  # Virtual barcode based on the invoice number

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.browse(docids)
        company = self.env.company
        return {
            'doc_ids': docids,
            'doc_model': 'assignment2.invoice',
            'docs': docs,
            'company': company,
        }
