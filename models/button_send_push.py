from odoo import models, fields, api
import xmlrpc.client
import logging
import base64

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    oferta = fields.Char(string="Tipo de Oferta", help="Descripción de oferta")
    enviar_push = fields.Boolean(string="Enviar Oferta", help="Si esta habilitado periodicamente se enviaran estas notificaciones al cliente")

    def boton_enviar_notificacion(self):
        """Enviar notificación manualmente desde el botón en product.template."""
        clientes = self.env['res.partner'].search([('app_server_url', '!=', False)])
        for cliente in clientes:
            rpc_url = cliente.app_server_url  # URL del servidor cliente
            try:
                server = xmlrpc.client.ServerProxy(rpc_url)

                # Generar el mensaje con el tipo de oferta
                mensaje = f"Hola {cliente.name}, ¡{self.oferta}! Producto: {self.name}"

                # Convertir la imagen a base64 para enviarla
                if self.image_1920:
                    imagen_base64 = base64.b64encode(self.image_1920).decode('utf-8')  # Imagen en base64
                else:
                    imagen_base64 = None  # Sin imagen

                # Enviar datos al servidor
                resultado = server.recibir_notificacion({
                    'mensaje': mensaje,
                    'imagen': imagen_base64,
                })

                if resultado:
                    _logger.info(f"Notificación enviada a {cliente.name}")
                else:
                    _logger.warning(f"{cliente.name} no confirmó recepción.")
            except Exception as e:
                _logger.error(f"Error al enviar notificación a {cliente.name}: {e}")


   ####################
#    #esta puede ser la accion planificada
#    def enviar_notificaciones_programadas(self):
#         """Envío automático de notificaciones para productos con 'enviar_push' activado."""
#         productos = self.search([('enviar_push', '=', True)])
#         clientes = self.env['res.partner'].search([('app_server_url', '!=', False)])

#         for producto in productos:
#             for cliente in clientes:
#                 rpc_url = cliente.app_server_url  # URL del servidor cliente
#                 try:
#                     server = xmlrpc.client.ServerProxy(rpc_url)

#                     # Generar el mensaje con el tipo de oferta
#                     mensaje = f"Hola {cliente.name}, ¡{producto.oferta}! Producto: {producto.name}"

#                     # Convertir la imagen del producto a base64
#                     imagen_base64 = None
#                     if producto.image_1920:
#                         imagen_base64 = base64.b64encode(producto.image_1920).decode('utf-8')

#                     # Enviar datos al servidor
#                     resultado = server.recibir_notificacion({
#                         'mensaje': mensaje,
#                         'imagen': imagen_base64,
#                     })

#                     if resultado:
#                         _logger.info(f"Notificación enviada a {cliente.name} sobre {producto.name}")
#                     else:
#                         _logger.warning(f"{cliente.name} no confirmó la recepción de la notificación de {producto.name}")
#                 except Exception as e:
#                     _logger.error(f"Error al enviar notificación a {cliente.name}: {e}")



    

