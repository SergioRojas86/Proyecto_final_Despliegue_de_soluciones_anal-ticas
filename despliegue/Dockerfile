FROM python:3.10

# Crear usuario que ejecuta la app
RUN adduser --disabled-password --gecos '' api-user

# Definir directorio de trabajo
WORKDIR /opt/dashboard

# Instalar dependencias
ADD ./dashboard /opt/dashboard/
RUN pip install --upgrade pip
RUN pip install -r /opt/dashboard/requirements.txt

# Cambiar propiedad de la carpeta a api-user
RUN chown -R api-user:api-user ./

USER api-user
# Puerto a exponer para la api 
EXPOSE 8050

# Comandos a ejecutar al correr el contenedor
CMD ["python3", "application.py"]
