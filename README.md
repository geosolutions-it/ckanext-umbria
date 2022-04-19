[![Tests](https://github.com/geosolutions-it/ckanext-umbria/workflows/Tests/badge.svg?branch=main)](https://github.com/geosolutions-it/ckanext-umbria/actions)

# ckanext-umbria

Custom extension for Regione Umbria.

Based on [ckanext-geosolutions-ui](https://github.com/geosolutions-it/ckanext-geosolutions-ui/tree/0cc7733cb8493e62189b48fba1ab555c8aa88e23)

## Installation

### With CKAN virtualenv in Linux Machine

1. Activate your CKAN virtual environment, for example:
    ```
     . /usr/lib/ckan/default/bin/activate
    ```
2. Clone the source and install it on the virtualenv
    ```
    git clone https://github.com/geosolutions-it/ckanext-umbria.git
    cd ckanext-umbria
    pip install -r requirements.txt
    pip install -e .
    ```
3. Add `umbria` to the `ckan.plugins` setting in your CKAN ini file

    ```
    vim /etc/ckan/default/ckan.ini
    ```

4. Add `umbria_dcat_ap` to the `ckanext.dcat.rdf.profiles` setting in your CKAN ini file,
   so that it reads:

    ```
    ckanext.dcat.rdf.profiles = euro_dcat_ap it_dcat_ap umbria_dcat_ap
    ```

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:
     ```
     sudo service apache2 reload
     ```

### With Docker

#### ckan docker setup
- install a ckan instance locally with docker (steps from ckan documentation https://docs.ckan.org/en/2.9/maintaining/installing/install-from-docker-compose.html)
#### add an extension inside docker of ckan
1. clone the umbria extension repository
    ```
    cd /path/to/my/projects
    git clone --recursive https://github.com/geosolutions-it/ckanext-umbria.git

    ```
2. to link ckan extension to ckan, create a file docker-compose.override.yml in /ckan/contrib/docker with the following code

    ```
    cd /path/to/my/projects/ckan/contrib/docker
    touch  docker-compose.override.yml

    ```
3. copy this configuration in docker-compose.override.yml
    ```
    version: '3'
    services:
    ckan:
        volumes:
        - '../../../ckanext-umbria:/usr/lib/ckan/venv/src/ckanext-umbria'

    ```
4. stop & start up the application

    ```
    docker-compose stop
    docker-compose up -d

    ```
5. get the id of the docker_ckan container with docker ps
    ```
    docker ps
    ```
6. attach the shell of the ckan docker container
    ```
    docker exec -it {my_docker_ckan_id} bash
    ```
7. activate the venv and navigate to the src folder inside the docker container
    ```
    #this command have to run inside docker
    source $CKAN_VENV/bin/activate && cd $CKAN_VENV/src/
    ```
8. install the extension

    ```
    #this command have to run inside docker
    cd ckanext-umbria
    pip install -e .
    ```
9. install ckan dev requirements
    ```
    #this command have to run inside docker
    cd ../ckan
    pip install -r dev-requirements.txt
    ```
#### enable development enviroment

1. add the plugin to the production.ini config

    ```
    #this command have to run inside docker
    vim /etc/ckan/production.ini
    ```
2. append the name of plugin in the list and set debug equal true (both are in the file)

    ```
    debug = true
    ....

    ckan.plugins = stats text_view image_view recline_view umbria
    ```
3. detach from docker container bash shell and restart ckan docker

    ```
    docker-compose restart ckan
    ```
## Usage

- inside the extension directory
    ```
    cd ckanext-umbria
    ```
- folder tree
    ```
    ├── __init__.py
    ├── __init__.pyc
    ├── i18n
    ├── less
    │   ├── custom.less
    │   ├── main.less
    │   └── variables.less
    ├── package-lock.json
    ├── package.json
    ├── plugin.py
    ├── plugin.pyc
    ├── public
    │   └── base
    │       ├── css
    │       │   └── main.css
    │       └── img
    │           ├── jumbotron_hp.jpg
    │           └── logo.png
    └── templates
        ├── base.html
        ├── footer.html
        ├── header.html
        └── home
            ├── index.html
            ├── layout.html
            └── snippets
                ├── item.html
                ├── search.html
                └── topics.html
    ```

- install npm dependecies
    ```
    npm install
    ```

- run less compiler
    ```
    npm run watch-less
    ```
Start to customize

1. Style

In the less folder, is possibile change the less variables, to have a basic style customization.

- less/variables.less

    ```
    @brandDefaultColor: #fff;
    @brandPrimaryColor: #3A79AF;
    @brandSecondaryColor: #f3f3f3;
    @brandNotificationColor:#62AE4A;
    @bodyTextColor:#464646;
    @brandNotificationColorTransparency: rgba(58, 121, 175, 0.9);
    @jumbotronBg: '../../../base/img/jumbotron_hp.jpg';
    @jumbotronBgSize: 1224px 613px;
    @jumbotronBgPosition: center -40px;
    @jumbotronMinHeight: 410px;
    @bgPath: e("");
    @layoutFontFamily: "Helvetica Neue", Arial, sans-serif;
    ```
2. Logo

To change the logo file, in header and footer override the file

- public/base/img/logo.png 
 
or change the logo var in

- templates/footer.html 
- templates/header.html

    ```
        {% set logo = '/base/img/logo.png' %}
    ```

3. Change footer info

    templates/footer.html change this var

    ```
        {% set logo = '/base/img/logo.png' %}
        {% set domain = 'http://www.regione.umbria.it/' %}
        {% set customer = 'About Regione Umbria' %}
        {% set landingPage = 'about' %}
        {% set powerdByDomain = 'https://www.geosolutionsgroup.com/' %}
        {% set powerdBy = 'GeoSolutions' %}
    ```
4. Minimize main.css file

    ```
        npm run compile-css
    ```


## Tests

To run the tests, do:
    ```
    pytest --ckan-ini=test.ini
    ```


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
