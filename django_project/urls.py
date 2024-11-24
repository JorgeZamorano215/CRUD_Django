"""
URL configuration for CursoDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Models.Alumno.views import FormularioAlumnoView


from Views.HomeView import HomeView
from apps.logeo import views

urlpatterns = [
        path('admin/', admin.site.urls),
    path('', HomeView.home, name='home'),
    path('login/', views.inicioSession, name='login'),
    path('CambioPassword/', views.cambioPassword, name='CambioPassword'),
    path('Inicio/', views.inicio, name='Inicio'),
    path('listarUsuarios/', views.listar_usuarios, name='listarUsuarios'),
    path('registrarUsuarios/', views.registrar_usuarios, name='registrarUsuarios'),
    path('editarusuarios/<int:id_usuario>', views.editar_usuarios, name='editarusuarios'),
    path('aplicareditarusuarios/<int:id_usuario>', views.aplicar_editar_usuarios, name='aplicareditarusuarios'),
    path('validareliminarusuario/<int:id_usuario>', views.validar_eliminar_usuarios, name='validareliminarusuario'),
    path('eliminarusuario/<int:id_usuario>', views.eliminar_usuario, name='eliminarusuario'),
    
    path('listarPersonas/', views.listar_personas, name='listarPersonas'),
    path('registrarPersonas/', views.registrar_personas, name='registrarPersonas'),
    path('validarRegistrarPersonas/<str:curp>/<int:tp>', views.validar_registrar_personas, name='validarRegistrarPersonas'),
    path('validarEditarPersonas/<str:curp>/<int:tp>', views.validar_editar_personas, name='validarEditarPersonas'),
    path('eliminarPersonas/<int:id_persona>', views.eliminar_persona, name='eliminarPersonas'),
    path('confirmarEliminarPersonas/<int:id_persona>', views.confirmacion_eliminar_persona, name='confirmarEliminarPersonas'),
    path('aplicarEliminarPersona/<int:id_persona>', views.aplicar_eliminar_persona, name='aplicarEliminarPersona'),
    path('editarPersona/<int:id_persona>/<int:id_direccion>', views.editar_personas, name='editarPersona'),
    path('aplicarEditarPersona/<int:id_persona>/<int:id_direccion>', views.aplicar_editar_personas, name='aplicarEditarPersona'),
    
    path('buscar_catalogo/<str:busqueda>/', views.buscar_catalogo, name='buscar_catalogo'),
    
    path('listarCatalagosVacio/', views.listar_catalagos_vacio, name='listarCatalagosVacio'),
    path('listarCatalagos/<str:modelo_nombre>', views.listar_catalagos, name='listarCatalagos'),
    path('listarCatalagosBuscar/<str:busqueda>', views.listar_catalagos_buscar, name='listarCatalagosBuscar'),
    path('registrarCatalagos/<str:modelo_nombre>', views.registrar_catalagos, name='registrarCatalagos'),
    path('editarCatalagos/<str:modelo_nombre>/<int:id_catalago>', views.editar_catalagos, name='editarCatalagos'),
    path('aplicareditarCatalagos/<str:modelo_nombre>/<int:id_catalago>', views.aplicar_editar_catalagos, name='aplicareditarCatalagos'),
    path('eliminarCatalagos/<int:id_catalago>', views.eliminar_catalagos, name='eliminarCatalagos'),
    path('confirmarEliminarCatalagos/<int:id_catalago>', views.confirmacion_eliminar_catalagos, name='confirmarEliminarCatalagos'),
    path('aplicarEliminarCatalagos/<int:id_catalago>', views.aplicar_eliminar_catalagos, name='aplicarEliminarCatalagos'),
    
    path('listarAplicaciones/', views.listar_aplicaciones, name='listarAplicaciones'),
    path('validarCvaplicaciones/<str:Cvaplicacion>', views.validar_Cvaplicaciones, name='validarCvaplicaciones'),
    path('registrarAplicaciones/', views.registrar_aplicaciones, name='registrarAplicaciones'),
    path('editarAplicaciones/<int:id_aplicacion>', views.editar_aplicaciones, name='editarAplicaciones'),
    path('aplicarEditarAplicaciones/<int:id_aplicacion>', views.aplicar_editar_aplicaciones, name='aplicarEditarAplicaciones'),
    path('validareliminaraplicaciones/<str:id_aplicacion>', views.validar_eliminar_aplicaciones, name='validareliminaraplicaciones'),
    path('eliminaraplicaciones/<int:id_aplicacion>', views.eliminar_aplicaciones, name='eliminaraplicaciones'),
    
    path('listaraccesos/', views.listar_accesos, name='listaraccesos'),
    path('listaraccesos2/<int:id_usuario>', views.listar_accesos2, name='listaraccesos2'),
    path('registraraccesos/<int:id_usuario>/<str:lista>', views.registrar_accesos, name='registraraccesos'),
    
    path('listarproductos/', views.listar_productos, name='listarproductos'),
    path('registrarproductos/', views.registrar_productos, name='registrarproductos'),
    path('editarproductos/<int:id_Producto>', views.editar_productos, name='editarproductos'),
    path('eliminarproductos/<int:id_Producto>', views.eliminar_productos, name='eliminarproductos'),
    path('aplicareliminarproductos/<int:id_Producto>', views.aplicar_eliminar_productos, name='aplicareliminarproductos'),
    
    path('venta/', views.venta, name='venta'),
    path('api/productos/<str:Codigo>/', views.ProductoCodigo, name='producto_codigo'),
    path('api/AlertaStock/<str:Codigo>/<int:Cantidad>/', views.AlertaStock, name='AlertaStock'),
    path('realizarventa/', views.procesar_venta, name='procesar_venta'),
    
    path('pedido/', views.Pedido, name='pedido'),
    path('api/proveedor_productos/<int:proveedor_id>/', views.proveedor_productos, name='proveedor_productos'),
    path('api/precioCompra_producto/<str:producto_ds>/', views.precioCompra_producto, name='precioCompra_producto'),
    path('realizarpedido/', views.procesar_pedido, name='procesar_pedido'),
    
    path('reportes/', views.Reportes, name='reportes'),
    path('detalleVenta/<int:venta_id>/', views.detalleVenta, name='detalleVenta'),
    path('detallePedido/<int:pedido_id>/', views.detallePedido, name='detallePedido'),
    path('detalleCompra/<int:compra_id>/', views.detalleCompra, name='detalleCompra'),
    path('api/ReportePeriodoVentas/<str:FecIni>/<str:FecFin>/', views.ReportePeriodoVentas, name='ReportePeriodoVentas'),
    path('api/ReportePeriodoPedidos/<str:FecIni>/<str:FecFin>/', views.ReportePeriodoPedidos, name='ReportePeriodoPedidos'),
    path('api/ReportePeriodoCompras/<str:FecIni>/<str:FecFin>/', views.ReportePeriodoCompras, name='ReportePeriodoCompras'),
    path('api/ReportePeriodoEfectivo/<str:FecIni>/<str:FecFin>/', views.ReportePeriodoEfectivo, name='ReportePeriodoEfectivo'),
    path('api/ReportePeriodoCaducidad/<str:FecIni>/<str:FecFin>/', views.ReportePeriodoCaducidad, name='ReportePeriodoCaducidad'),
    
    path('RecepcionPedidos/', views.RecepcionPedidos, name='RecepcionPedidos'),
    path('api/CodigoPedidoRecepcion/<int:pedido_id>/', views.CodigoPedidoRecepcion, name='CodigoPedidoRecepcion'),
    path('realizarRecepcion/', views.procesar_recepcion, name='procesar_recepcion'),
    
    path('CorteCaja/', views.CorteCaja, name='CorteCaja'),
    path('api/CalcularCorteCaja/<str:FecIni>/<str:FecFin>/', views.CalcularCorteCaja, name='CalcularCorteCaja'),
    path('realizarCorteCaja/', views.procesar_corteCaja, name='procesar_corteCaja'),
    
    path('listarCajaGrande/', views.listar_CajaGrande, name='listarCajaGrande'),
    path('realizarGasto/', views.procesar_gasto, name='procesar_gasto'),
    path('Menu/', views.Menu, name='Menu'),
    
    path('signup/', views.signup, name='signup'),
    path('pagina/', HomeView.pagina1, name='pagina1'),
    path('pagina2/<int:parametro1>', HomeView.pagina2, name='pagina2'),
    path('pagina3/<int:parametro1>/<int:parametro2>', HomeView.pagina3, name='pagina3'),
    path('formulario/', HomeView.formulario, name='formularioPrueba'),
    path('crear-superusuario/', FormularioAlumnoView.create_superuser_view, name='crear_superusuario'),
    path('registrarAlumno/', FormularioAlumnoView.index, name='registrarAlumno'),
    path('guardarAlumno/', FormularioAlumnoView.procesar_formulario, name='guardarAlumno'),
    path('listarAlumnos/', FormularioAlumnoView.listar_alumnos, name='listarAlumnos'),
    path('editarAlumnos/<int:id_alumno>', FormularioAlumnoView.edit, name='editarAlumnos'),
    path('actualizarAlumnos/<int:id_alumno>', FormularioAlumnoView.actualizar_alumno, name='actualizarAlumnos'),
    path('eliminarAlumnos/<int:id_alumno>', FormularioAlumnoView.delete, name='eliminarAlumnos'),
    
]
