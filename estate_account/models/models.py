from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError


class Property(models.Model):
    _inherit = "estate.property"

    # override sold action
    def set_sold(self):

        if self.env.user.has_group('account.group_account_invoice'):
            # check if the user is in group billing
            try:
                self.check_access_rights('write')
                self.check_access_rights('create')
            except AccessError:
                raise UserError(_("You don't have the access rights needed to update or create a invoice"))

            # check access rules
            self.check_access_rule('create')

            journal = self.env['account.journal'].search([('type', '=', 'sale')])[0]

            # create invoice line
            invoice_lines = [
                {
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": (self.selling_price * 6) / 100
                },
                {
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100
                }
            ]
            print(" reached ".center(100, '='))
            self.env['account.move'].sudo().create({
                'partner_id': self.buyer.id,
                'move_type': "out_invoice",
                'journal_id': journal.id,
                'invoice_line_ids': invoice_lines
            })

            return super().set_sold()
        else:
            raise UserError(_("You don't have the access needed"))
