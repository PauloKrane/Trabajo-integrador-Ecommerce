from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Comprador(models.Model):
    idComprador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, blank=False, null=False)
    apellido = models.CharField(max_length=45, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    telefono = models.CharField(max_length=15, blank=True, null=False, validators=[MinValueValidator(0)] )
    contrasenia = models.CharField(max_length=8, blank=False, unique=True, null=False)
   
    class Meta:
        db_table = 'Comprador'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return f'Cliente: {self.apellido} {self.nombre}'

class Recibo(models.Model):
    PREPARAR = 'PRE'
    PROCESADO = 'PRO'
    ENVIADO = 'ENV'
    ENTREGADO = 'ENT'
    CANCELADO = 'CAN'
    ESTADO_CHOICES = [
        (PREPARAR, 'Preparar'),
        (PROCESADO, 'Procesado'),
        (ENVIADO, 'Enviado'),
        (ENTREGADO, 'Entregado'),
        (CANCELADO, 'Cancelado'),
    ]

    idRecibo = models.AutoField(primary_key=True)
    fechaHoraEmitida = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(0)])
    estadoPedido = models.CharField(max_length=3, choices= ESTADO_CHOICES, default=PREPARAR, null=False)
    kfComprador = models.ForeignKey(Comprador, to_field='idComprador', on_delete=models.CASCADE)
     
    class Meta:
        db_table = 'Recibo'
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'

    def __str__(self):
        return f'Código recibo #{self.idRecibo} - Cliente: {self.kfComprador.apellido} {self.kfComprador.nombre} - Estado pedido: {self.get_estadoPedido_display()} ({self.estadoPedido}) '
        
class DetalleRecibo(models.Model):
    idDetalleRecibo = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=45, blank=False, null=False)
    cantidad = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    precioUnitario = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(0)])
    kfRecibo = models.ForeignKey(Recibo, to_field='idRecibo', on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'DetalleRecibo'
        verbose_name = 'Detalle de Recibo'
        verbose_name_plural = 'Detalles de Recibo'

    def __str__(self):
        return f'Código detalle recibo #{self.idDetalleRecibo} - Código recibo #{self.kfRecibo}'
    
class DetalleEnvio(models.Model):
    idDetalleEnvio = models.AutoField(primary_key=True)
    fechaEnvio = models.DateField(blank=False, null=False)
    direccionEnvio = models.CharField(max_length=100, blank=False, null=False )
    detalleEntrega = models.CharField(max_length=300, blank=True, null=True)
    kfRecibo = models.ForeignKey(Recibo, to_field='idRecibo', on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'DetalleEnvio'
        verbose_name = 'Detalle de envío'
    def __str__(self):
        return f'Cliente: {self.kfRecibo.kfComprador.nombre} - Fecha de Envío: {self.fechaEnvio} - Dirección: {self.direccionEnvio}'

class ChatConsulta(models.Model):
    idChatConsulta = models.AutoField(primary_key=True)
    fechaCreada = models.DateField(auto_now_add=True)
    kfComprador = models.ForeignKey(Comprador, to_field='idComprador', on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'ChatConsulta'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f'Consulta generada #{self.fechaCreada} - Usuario: {self.kfComprador.nombre} {self.kfComprador.apellido}'

class Consultas(models.Model):
    idConsulta = models.AutoField(primary_key=True)
    fechaHoraEnviado = models.DateTimeField(auto_now_add=True)
    mensaje = models.CharField(max_length=500, blank=False, null=False)
    kfChatConsulta = models.ForeignKey(ChatConsulta, to_field='idChatConsulta', on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'Consultas'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f'Mensaje #{self.mensaje} - Enviado: {self.fechaHoraEnviado}'

class Categorias(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=30, blank=False, null=False)
   
    class Meta:
        db_table = 'Categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return f'Categoría #{self.nombreCategoria}'

class Productos(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=25, blank=False, null=False)
    descripcionProducto = models.CharField(max_length=255, blank=False, null=False)
    costoProducto = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(0)])
    precioProducto = models.DecimalField(max_digits=7, decimal_places=2, blank=False, null=False, validators=[MinValueValidator(0)])
    stockProducto = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    imagenProducto = models.ImageField(upload_to='imagenes/', blank=False, null=False)
    fechaIngreso = models.DateField(auto_now_add=True)
    fechaActualizacion = models.DateField(auto_now=True)
    kfCategoria = models.ForeignKey (Categorias, to_field='idCategoria', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'Código #{self.idProducto} - Producto:{self.nombreProducto} - Descripción:{self.descripcionProducto} - Costo:{self.costoProducto} - Precio:{self.precioProducto} - Stock:{self.stockProducto} - Imagen:{self.imagenProducto} - Ingreso:{self.fechaIngreso} - Actualizo:{self.fechaActualizacion}'
    
class ValoracionProducto(models.Model):
    idValoracionProducto = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=300, blank=True, null=True)
    calificacion = models.IntegerField(validators=[MaxValueValidator(limit_value=5)])
    fechaCalificacion = models.DateField(auto_now_add=True)
    kfComprador = models.ForeignKey(Comprador, to_field='idComprador', on_delete=models.CASCADE)
    kfProducto = models.ForeignKey(Productos, to_field='idProducto', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ValoracionProducto'
        verbose_name = 'Valoración'
        verbose_name_plural = 'Valoraciones'

    def __str__(self):
        return f'Cliente:{self.kfComprador.nombre} {self.kfComprador.apellido} - Producto:{self.kfProducto.nombreProducto} - Comentario:{self.comentario} - Calificación:{self.calificacion} - Calificado:{self.fechaCalificacion}'
    
class Carrito(models.Model):
    idCarrito = models.AutoField(primary_key=True)
    cantidadProducto = models.IntegerField(blank=False, null=False, default=0, validators=[MinValueValidator(0)])
    kfComprador = models.ForeignKey(Comprador, to_field='idComprador', on_delete=models.CASCADE)
    kfProducto = models.ForeignKey(Productos, to_field='idProducto', on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'Carrito'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f'Cliente:{self.kfComprador.nombre} {self.kfComprador.apellido} - Producto:{self.kfProducto.nombreProducto} - Precio:{self.kfProducto.precioProducto} - Cantidad:{self.cantidadProducto}'

class Administrador (models.Model):
    idAdministrador = models.AutoField(primary_key=True)
    nombreAdministrador = models.CharField(max_length=25,blank=False, null=False)
    apellidoAdministrador = models.CharField(max_length=45, blank=False, null=False)
    contraseniaAdministrador = models.CharField(max_length=8, blank=False, unique=True, null=False)
    emailAdministrador = models.EmailField(blank=False, null=False)

    class Meta:
        db_table = 'Administrador'
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

    def __str__(self):
        return f'Administrador:{self.nombreAdministrador} {self.apellidoAdministrador}'

