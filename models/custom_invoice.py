from odoo import models, fields, api

class CustomInvoice(models.Model):
    _name = 'custom_invoicing.invoice'
    _description = 'Custom Invoices'

    customer_id = fields.Many2one('res.partner', string='Customer')
    order_number = fields.Char(string='Order Number')
    due_date = fields.Date(string='Due Date')
    reference = fields.Char(string='Reference')
    product_line_ids = fields.Many2many('product.management.product', string='Product Lines')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ], default='draft', string='Status')

    @api.model
    def send_invoice_email(self):
        for invoice in self:

            # Generate the PDF invoice report
            pdf_content, _ = self.env.ref('custom_invoicing.report_invoice').sudo()._render_qweb_pdf([invoice.id])

            # Send the email with the PDF attachment
            template = self.env.ref('custom_invoicing.email_template_custom_invoice')
            template.send_mail(invoice.id, force_send=True)

        self.write({'state': 'sent'})


