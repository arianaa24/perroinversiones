# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class ReplicaWizard(models.TransientModel):
    _name = 'replica.wizard'

    tipo_replicacion = fields.Selection(string='Tipo de Replicación', required=True, selection=[
            ('dia', 'Día'),
            ('semana', 'Semana'),
            ('mes', 'Mes'),
        ])
    numero_veces = fields.Integer(string='Número de veces', required=True)
    order_id = fields.Many2one('sale.order', string='Orden de venta original', required=True)

    @api.constrains('numero_veces')
    def _check_numero_veces(self):
        for record in self:
            if record.numero_veces > 12 or record.numero_veces < 1:
                raise ValidationError("El número de veces debe ser entre 1 y 12.")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            res.update({
                'order_id': active_id,
            })
        return res
    
    def replicar(self):
        self.ensure_one()
        fecha_base = self.order_id.date_order
        rental_start_base = self.order_id.rental_start_date
        rental_return_base = self.order_id.rental_return_date

        for i in range(1, self.numero_veces + 1):
            if self.tipo_replicacion == 'dia':
                nueva_fecha = fecha_base + timedelta(days=i)
                nueva_rental_start_date = rental_start_base + timedelta(days=i)
                nueva_rental_return_base = rental_return_base + timedelta(days=i)
            elif self.tipo_replicacion == 'semana':
                nueva_fecha = fecha_base + timedelta(weeks=i)
                nueva_rental_start_date = rental_start_base + timedelta(weeks=i)
                nueva_rental_return_base = rental_return_base + timedelta(weeks=i)
            elif self.tipo_replicacion == 'mes':
                nueva_fecha = fecha_base + relativedelta(months=i)
                nueva_rental_start_date = rental_start_base + relativedelta(months=i)
                nueva_rental_return_base = rental_return_base + relativedelta(months=i)

            self.order_id.copy({
                'date_order': nueva_fecha,
                'rental_start_date': nueva_rental_start_date,
                'rental_return_date': nueva_rental_return_base,
                'origin': f'{self.order_id.name} (Replicada #{i})',
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Órdenes replicadas',
                'message': f'Se replicaron {self.numero_veces} órdenes con éxito.',
                'type': 'success',
                'sticky': False,
            }
        }