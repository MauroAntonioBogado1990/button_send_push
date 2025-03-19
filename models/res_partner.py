from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    rpc_url = fields.Char(string="URL XML-RPC", help="URL del servidor XML-RPC del cliente para recibir notificaciones.")
