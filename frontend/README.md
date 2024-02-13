# CALI Project

Introducción del proyecto ...

## Pasos para ejecutar el frontend en modo desarrollador por primera vez

Para iniciar el proyecto se deben seguir los siguientes pasos:

1. Tener instalado nvm o npm

- npm (Node Package Manager): Se pueden seguir los pasos de [link](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- nvm (Node Version Manager): Se pueden seguir los pasos de [link](https://github.com/nvm-sh/nvm), y ejecutar el comando:

  `nvm install latest`

1. Verificar que se tiene instalado npm, ejecutando el código:

   `npm --version`

1. Ubicarse en la carpeta del proyecto: **\project-cali\frontend** y ejecutar el comando:

   `npm install`

1. Copiar el archivo ubicado en **\project-cali\frontend\env** en **\project-cali\frontend** y cambiar le nombre a **.env**

1. Configurar las variables de entorno de acuerdo con el proyecto.

- **REACT_APP_STATUS**: Puede ser "dev" o "prod", dependiendo del ambiente
- **REACT_APP_DEV_API_URL**: Link del API para desarrollo
- **REACT_APP_PROD_API_URL**: Link del API para producción
- **REACT_APP_DEV_GRAFANA_TABS**: Arreglo de strings el cual contienen las direcciones de grafana para las pertañas de monitoreo en desarrollo
- **REACT_APP_PROD_GRAFANA_TABS**: Arreglo de strings el cual contienen las direcciones de grafana para las pertañas de monitoreo en producción
- **REACT_APP_TITLE**: Nombre del proyecto

5. Ejecutar el comando:

   `npm start`
