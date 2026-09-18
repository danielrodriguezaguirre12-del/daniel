# API de Autos y Reservas — FastAPI + AWS EC2

API RESTful con FastAPI que implementa operaciones CRUD para dos entidades: **Autos** y **Reservas**, usando SQLModel como ORM sobre SQLite.

## Entidades

**Auto**: `id`, `marca`, `modelo`, `anio`, `placa`, `disponible`

**Reserva**: `id`, `auto_id` (FK a Auto), `cliente`, `fecha_inicio`, `fecha_fin`, `estado`

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Mensaje de bienvenida |
| POST | `/autos/` | Crear auto |
| GET | `/autos/` | Listar autos |
| GET | `/autos/{id}` | Obtener auto por ID |
| PUT | `/autos/{id}` | Actualizar auto |
| DELETE | `/autos/{id}` | Eliminar auto |
| POST | `/reservas/` | Crear reserva |
| GET | `/reservas/` | Listar reservas |
| GET | `/reservas/{id}` | Obtener reserva por ID |
| PUT | `/reservas/{id}` | Actualizar reserva |
| DELETE | `/reservas/{id}` | Eliminar reserva |

Documentación automática disponible en `/docs` (Swagger) y `/redoc`.

---

## 1. Repositorio en GitHub

```bash
git init
git add .
git commit -m "API de Autos y Reservas con FastAPI"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

## 2. Entorno local

```bash
python3 -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Probar localmente

```bash
python main.py
# o
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Abre `http://127.0.0.1:8000/docs` para probar los endpoints.

---

## 4. Crear la instancia EC2

1. En la consola de AWS, ve a **EC2 → Launch Instance**.
2. Elige una AMI, por ejemplo **Ubuntu Server 22.04 LTS**.
3. Tipo de instancia: `t2.micro` (elegible para capa gratuita) es suficiente.
4. Crea o selecciona un **par de claves (.pem)** para conectarte por SSH — descárgalo y guárdalo bien.
5. En **Configuración de red / Security Group**, agrega estas reglas de entrada (Inbound rules):
   - `SSH` – puerto `22` – origen: tu IP (o `0.0.0.0/0` si prefieres, menos seguro)
   - `Custom TCP` – puerto `8000` – origen: `0.0.0.0/0` (para que la API sea pública)
6. Lanza la instancia y espera a que esté en estado "running". Copia su **IP pública**.

## 5. Conectarse a la instancia

```bash
chmod 400 tu-clave.pem
ssh -i "tu-clave.pem" ubuntu@<IP-PUBLICA-EC2>
```

## 6. Instalar dependencias en la instancia

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y

# Node.js y pm2 (para mantener la API corriendo en segundo plano)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g pm2
```

## 7. Clonar el repositorio y preparar el proyecto

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 8. Ejecutar la API con pm2

Como pm2 corre procesos de Node por defecto, para ejecutar un proceso Python le indicamos el intérprete directamente:

```bash
pm2 start venv/bin/uvicorn --name autos-reservas-api -- main:app --host 0.0.0.0 --port 8000
```

Comandos útiles de pm2:

```bash
pm2 list                     # ver procesos activos
pm2 logs autos-reservas-api  # ver logs en vivo
pm2 restart autos-reservas-api
pm2 stop autos-reservas-api
pm2 save                     # guardar la lista de procesos
pm2 startup                  # generar el comando para que pm2 inicie con el sistema (ejecútalo tal cual lo indique)
```

## 9. Probar la API públicamente

Desde tu navegador o Postman:

```
http://<IP-PUBLICA-EC2>:8000/
http://<IP-PUBLICA-EC2>:8000/docs
http://<IP-PUBLICA-EC2>:8000/autos/
http://<IP-PUBLICA-EC2>:8000/reservas/
```

> Si no carga, revisa que el Security Group tenga abierto el puerto `8000` y que pm2 muestre el proceso como `online` (`pm2 list`).

---

## 10. Entrega

- Link del repositorio (GitHub/GitLab) con todos los cambios subidos (`git push`).
- URL pública de la API funcionando: `http://<IP-PUBLICA-EC2>:8000/`
- Video explicando el desarrollo y el despliegue.

## Notas

- La IP pública de una instancia EC2 cambia si la detienes y la vuelves a iniciar, a menos que le asignes una **Elastic IP** (recomendado para que la URL no cambie).
- Recuerda no exponer el archivo `.pem` ni subirlo al repositorio.
