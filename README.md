# nodes_catalog

###Construir la imagen de docker con 
`docker build . -t selenium-chrome`

### Correr el contenedor con 
`docker run -v $PWD/data:/data -d -it selenium-chrome`

### Resultados
Los resultados se van a guardar en la carpeta `/data` con la fecha en formato `dd_mm_yyyy_catalogo_nodos.csv`
