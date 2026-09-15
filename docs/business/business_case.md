# Business Case

## 1. Contexto

Andes Commerce es una empresa ficticia de retail omnicanal. Comercializa productos a través de tiendas físicas y ecommerce.

La empresa posee información distribuida en diferentes sistemas:

- POS: operaciones de tiendas.
- Ecommerce: pedidos online.
- CRM: clientes.
- ERP: productos e inventario.
- Payments: pagos.

Actualmente existen procesos manuales para consolidar información.

## 2. Problema

La dirección no cuenta con una visión confiable y oportuna de ventas, inventario y rentabilidad.

El problema no es solamente técnico. La fragmentación de datos impacta la operación y la toma de decisiones.

## 3. Impacto

- Reportes que pueden mostrar cifras diferentes.
- Tiempo elevado para consolidar información.
- Dificultad para detectar riesgo de stock.
- Baja trazabilidad desde el reporte hasta la fuente.
- Mayor esfuerzo manual para analistas.

## 4. Usuarios

### Dirección comercial
Necesita evolución de ventas, margen y cumplimiento.

### Gerentes de tienda
Necesitan stock, rotación y rendimiento por sucursal.

### Equipo de BI
Necesita datasets consistentes y documentados.

### Data Engineering
Necesita pipelines trazables, medibles y recuperables.

## 5. Preguntas de negocio

1. ¿Cuál es el revenue por canal, tienda y categoría?
2. ¿Cuál es el margen por categoría?
3. ¿Qué productos presentan riesgo de quiebre?
4. ¿Qué tiendas tienen menor rotación?
5. ¿Cómo evoluciona el ticket promedio?
6. ¿Qué clientes disminuyen su frecuencia de compra?
7. ¿Qué promociones generan volumen pero deterioran margen?

## 6. Resultado esperado

Una plataforma que permita pasar de:

fuentes aisladas -> consolidación manual -> reportes

a:

fuentes -> pipelines -> datos confiables -> modelos Gold -> analítica.

## 7. Métricas de éxito

- porcentaje de registros válidos;
- cantidad de registros procesados;
- registros rechazados;
- freshness;
- diferencia entre conteos de origen y destino;
- tiempo de ejecución;
- disponibilidad de datasets Gold;
- cantidad de preguntas de negocio que pueden responderse sin reconciliación manual.
