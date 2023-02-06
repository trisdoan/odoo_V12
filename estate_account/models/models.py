from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError


class Property(models.Model):
    _inherit = "estate.property"

    # override sold action
    def set_sold(self):
        res = super().set_sold()
        invoice_lines = [
            {
                "name": self.buyer.id,
                "quantity": 1,
                "price_unit": (self.selling_price * 6) / 100
            },
            {
                "name": "Administrative fees",
                "quantity": 1,
                "price_unit": 100
            }
        ]
        if res:
            journal = self.env['account.journal'].search([('type', '=', 'sale')])[0]
            self.env['account.move'].sudo().create({
                'partner_id': self.buyer.id,
                'journal_id': journal.id,
                'invoice_line_ids': self.env["account.invoice"].create(invoice_lines)
            })
        print(" reached ".center(100, '='))
        return res
