from odoo import http
from odoo.http import request

class MyReportController(http.Controller):
    @http.route('/report/invoice', type='http', auth="user", website=True)
    def generate_report(self, custom_invoice_id):
        # Fetch the CustomInvoice record based on the custom_invoice_id
        custom_invoice_record = request.env['custom_invoicing.invoice'].search([])

        if custom_invoice_record:
            report_data = {
                'o': custom_invoice_record,
            }
            print(report_data)

            report = request.env.ref('custom_invoicing.my_custom_report_template').render(report_data)
            return report

        return "Custom Invoice not found."

