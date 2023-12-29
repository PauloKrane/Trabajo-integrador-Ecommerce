from django.contrib import admin
from .models import Comprador
from .models import Productos
from .models import Carrito
from .models import Categorias
from .models import ValoracionProducto
from .models import ChatConsulta
from .models import Consultas
from .models import Recibo
from .models import DetalleRecibo
from .models import DetalleEnvio
from .models import Administrador
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# Register your models here.

@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    pass

class CompradorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')

class ProductosAdmin(admin.ModelAdmin):
    list_display = ('idProducto', 'nombreProducto', 'descripcionProducto', 'costoProducto', 'precioProducto', 'stockProducto', 'imagenProducto', 'fechaIngreso', 'fechaActualizacion')

class CarritoAdmin(admin.ModelAdmin):
    list_display = ('idCarrito', 'cantidadProducto', 'kfComprador', 'kfProducto')

class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('idCategoria', 'nombreCategoria')

class ValoracionProductosAdmin(admin.ModelAdmin):
    list_display = ('idValoracionProducto', 'comentario', 'calificacion', 'fechaCalificacion', 'kfComprador', 'kfProducto')

class ChatConsultaAdmin(admin.ModelAdmin):
    list_display = ('idChatConsulta', 'fechaCreada', 'kfComprador')

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('idConsulta', 'fechaHoraEnviado', 'mensaje', 'kfChatConsulta')

class ReciboAdmin(admin.ModelAdmin):
    list_display = ('idRecibo', 'fechaHoraEmitida', 'total', 'estadoPedido', 'kfComprador')

class DetalleReciboAdmin(admin.ModelAdmin):
    list_display = ('idDetalleRecibo', 'nombreProducto', 'cantidad', 'precioUnitario', 'kfRecibo')

class DetalleEnvioAdmin(admin.ModelAdmin):
    list_display = ('idDetalleEnvio', 'fechaEnvio', 'direccionEnvio', 'detalleEntrega', 'kfRecibo')

class AdministradorAdmin (admin.ModelAdmin):
    list_display = ('idAdministrador', 'nombreAdministrador', 'apellidoAdministrador', 'emailAdministrador')

admin.site.register(Comprador, CompradorAdmin) 
admin.site.register(Productos, ProductosAdmin)  
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Categorias, CategoriasAdmin)
admin.site.register(ValoracionProducto, ValoracionProductosAdmin)
admin.site.register(ChatConsulta, ChatConsultaAdmin)
admin.site.register(Consultas, ConsultaAdmin)
admin.site.register(Recibo, ReciboAdmin)
admin.site.register(DetalleRecibo, DetalleReciboAdmin)
admin.site.register(DetalleEnvio, DetalleEnvioAdmin)
admin.site.register(Administrador, AdministradorAdmin)