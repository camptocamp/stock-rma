# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openerp import api, fields, models


class RmaOrder(models.Model):
    _inherit = "rma.order"

    @api.multi
    def _compute_sales_count(self):
        for rma in self:
            sales = rma.mapped('rma_line_ids.sale_line_id.order_id')
            rma.sale_count = len(sales)

    sale_count = fields.Integer(
        compute=_compute_sales_count, string='# of Sales')

    @api.model
    def _get_line_domain(self, rma_id, line):
        if line.sale_line_id and line.sale_line_id.id:
            domain = [('rma_id', '=', rma_id.id),
                      ('type', '=', 'supplier'),
                      ('sale_line_id', '=', line.sale_line_id.id)]
        else:
            domain = super(RmaOrder, self)._get_line_domain(rma_id, line)
        return domain

    @api.multi
    def action_view_sale_order(self):
        action = self.env.ref('sale.action_quotations')
        result = action.read()[0]
        so_ids = self.mapped('rma_line_ids.sale_line_id.order_id').ids
        result['domain'] = [('id', 'in', so_ids)]
        return result
