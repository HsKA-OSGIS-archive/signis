# (S)IGNIS
Repository for fictional company (S)IGNIS of HSKA OSGIS course WS.
This project is focussed in the development of a fire risk model and a web platform to visualize data related with fires, including the obtained model and allow the user the interaction with it. This project has been thougth as a tool for helping fire prevention and management.

## Getting Started

To start de application you can run the script [runserver.sh](https://github.com/HsKA-OSGIS/signis/blob/master/runserver.sh). It's a face to face with the software, guiding you throught the configuration of the application. 

### Prerequisites

It's hardly recommended that you have in your computer the following tools:
* Tomcat
* Geoserver
* Qgis 2
* PostgreSQL

NOTE: it's recommended to set the tomcat filter for CORS. In the web.xml, commonly stored in /opt/tomcat/conf/, type the following lines:
```
<filter>
  <filter-name>CorsFilter</filter-name>
  <filter-class>org.apache.catalina.filters.CorsFilter</filter-class>
  <init-param>
    <param-name>cors.allowed.origins</param-name>
    <param-value>*</param-value>
  </init-param>
  <init-param>
    <param-name>cors.allowed.methods</param-name>
    <param-value>GET,POST,HEAD,OPTIONS,PUT</param-value>
  </init-param>
  <init-param>
    <param-name>cors.allowed.headers</param-name>
    <param-value>Content-Type,X-Requested-With,accept,Origin,
Access-Control-Request-Method,Access-Control-Request-Headers</param-value>
  </init-param>
  <init-param>
    <param-name>cors.exposed.headers</param-name>
    <param-value>Access-Control-Allow-Origin,Access-Control-Allow-Credentials</param-value>
  </init-param>
</filter>
<filter-mapping>
  <filter-name>CorsFilter</filter-name>
  <url-pattern>/*</url-pattern>
</filter-mapping>
```

### Installing

To build the application you can run in the directory of the repository:

```
./runserver.sh
```
To configure the application, press the option 1 and follow the instructions. Then, you can open the browser in:
```
http://localhost:8000
```

## Model information
To see more information about the model go to the model [readme](https://github.com/HsKA-OSGIS/signis/blob/master/README_MODEL)

## Limitations

The project is builded with Django 1.11, Python 2 and you need to run the model QGIS 2.

## Built With

* [Django](https://www.djangoproject.com/) - The back end framework used


## Authors

* **Carlos Bayarri** - [CarlosBayarri](https://github.com/CarlosBayarri)
* **Raquel Luján** - [RaquelLujan](https://github.com/ralugar)
* **Jorge Hernández** - [JorgeHernandez](https://github.com/jorgeho1995)
* **Jesús Sanchez** - [JesusSanchez](https://github.com/jesusn95)
* **Raquel Arcon** - [RaquelArcon](https://github.com/rachelarna)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

