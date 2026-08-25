# Taller 1 · Calcular el IVA de una factura
# Estudiante: Bedoya Londoño Estefania

# ── Sistema de Facturación · Papelería El Recibo · v0.1 ──
# Curso: Lenguajes de Programación (FDE 058) · Semana 3 · Entrega individual calificada (Seguimiento 60 %).
# 
# Este cuaderno no es un ejercicio suelto: es la primera versión del sistema de facturación de la papelería. Al terminar, el programa atiende una venta de principio a fin —pide los datos en caja, calcula el impuesto y emite una factura con la marca del negocio y su número consecutivo— y cierra con el resumen de ventas del día.
# 
# Todo se resuelve con lo que ya sabes: datos con nombre, tipos, operaciones y mensajes en pantalla. Hoy no se usan funciones propias (def / function), decisiones (if) ni ciclos.

# ── La regla del negocio: el IVA ──
# El IVA (Impuesto al Valor Agregado) es un porcentaje que se suma al precio de venta. En Colombia la tarifa general es del 19 %.
# 
# El subtotal es lo que cuesta la mercancía sin impuesto (cantidad por valor unitario). El IVA sale de multiplicar ese subtotal por la tarifa en decimales (19 % = 0.19) y el total a pagar es la suma de ambos.
# Subtotal = cantidad x valor_unitario
# IVA = Subtotal x tarifa
# Total = Subtotal + IVA = Subtotal x (1 + tarifa)

# ── Cómo se trabaja este cuaderno ──
# Cada bloque es una parte del sistema y se ejecuta con ▶. Lo que creas en un bloque sigue vivo en los siguientes, igual que en un cuaderno de Colab o en un guion de RStudio.
# 
# Cuando tu programa pide un dato con input (Python) o readline (R), el cuaderno responde con los datos de prueba del panel de arriba, en el mismo orden en que los pides. Cámbialos y vuelve a ejecutar para atender otra venta.
# 
# Rotula cada bloque con un comentario (#) que diga qué hace. Un sistema sin rótulos es un sistema que nadie puede retomar mañana: eso también se califica.

# 1. Datos del negocio: guarda en variables el nombre de la papelería, su NIT, el número de la factura y la tarifa del IVA. Son los datos que no cambian en cada venta.
# Sistema de facturación - FITMETAC
# Autor: ESTEFANIA BEDOYA
# --- Datos del negocio ---
nombre_negocio <- "FITMETAC"
nit <- "908.859.425-9"
numero_factura <- 1
tarifa_iva <- 0.19

cat("Bienvenido al sistema de facturacion de", nombre_negocio)

# 2. Datos de entrada: el sistema atiende al cajero. Pídele el nombre del cliente, el producto, la cantidad, el valor unitario y cuánto cuesta lo mismo en la competencia.
# Datos de entra
cliente <- readline("Nombre del cliente: ")
producto <- readline("Producto: ")
cantidad_texto <- readline("Cantidad: ")
valor_texto <- readline("Valor unitario sin IVA: ")
competencia_texto <- readline("Precio total en la competencia: ")

# 3. Conversión de tipos: lo que entró es texto y con texto no se puede calcular. Conviértelo a número y muestra el tipo que quedó guardado.
#Conversión a número
cantidad <- as.numeric(cantidad_texto)
valor_unitario <- as.numeric(valor_texto)
total_competencia <- as.numeric(competencia_texto)

cat("Tipo de cantidad:", class(cantidad))
cat("Tipo de valor_unitario:", class(valor_unitario))

# 4. Proceso: calcula el subtotal, el IVA, el total a pagar y cuánto se ahorra el cliente frente a la competencia. Siempre con variables, nunca con números escritos a mano.
# --- Cálculos ---
subtotal <- cantidad * valor_unitario
iva <- subtotal * tarifa_iva
total <- subtotal + iva
ahorro <- total_competencia - total

# 5. Salida: imprime la factura. Encabezado con el negocio, el NIT y el número consecutivo; luego el cliente, el detalle del producto, el subtotal, el IVA, el TOTAL A PAGAR y el ahorro frente a la competencia.
#Salida
cat(nombre_negocio, "- NIT", nit, "-Numero_factura",numero_factura)
cat("================")
cat("cliente", cliente,"-producto",producto,"-cantidad",cantidad)
cat("================")
cat("Subtotal:", subtotal,"IVA (19%):", iva,"TOTAL A PAGAR:", total)
cat("================")
cat("Competencia:", total_competencia,"Ahorro del cliente:", ahorro)
cat("================")



# 6. Cierre de caja: registra dos ventas más del día, suma lo vendido y calcula el promedio por venta. Muestra el resumen.
#Cierre de caja
venta2 <- as.numeric(readline("Total de la segunda venta: "))
venta3 <- as.numeric(readline("Total de la tercera venta: "))

total_dia <- total + venta2 + venta3
promedio_dia <- (total + venta2 + venta3) / 3

cat("RESUMEN DEL DIA")
cat("Ventas registradas: 3")
cat("Total vendido:", total_dia)
cat("Promedio por venta:", promedio_dia)

# ── Cierre ──
# El sistema quedó completo: registra los datos del negocio, atiende al cajero, convierte, calcula, emite la factura con su consecutivo y cierra la caja del día.
# 
# Descarga el cuaderno con el botón ⬇ de la barra, publícalo en tu repositorio y pega el enlace en la casilla de entrega.
