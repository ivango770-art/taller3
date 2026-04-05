## 🗄️ Configuración de la Base de Datos

### Opción 1: Usar MySQL Workbench
1. Abre MySQL Workbench
2. Ejecuta el archivo `database.sql`
3. Verifica que la tabla se creó: `SELECT * FROM datosivan_taller;`

### Opción 2: Usar línea de comandos
```bash
mysql -u root -p < database.sql
