# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_replicar(self):
        if not self.rental_start_date or not self.rental_return_date:
            raise UserError("Debe asignar el período de alquiler antes de replicar la orden.")
        
        if not self.order_line:
            raise UserError("Debe agregar al menos una línea de producto antes de replicar la orden.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'replica.wizard.form',
            'res_model': 'replica.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': self.env.context,
        }