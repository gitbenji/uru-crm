# Ani Theme rewritten in Angular2 and Bootstrap 4

This project is a part of the famous ANI Theme [Ani Theme v2.0](http://www.strapui.com/themes/ani-angular-2-bootstrap-4-theme/) to Angular2 Theme.

Powered by [StartAngular](http://startangular.com/) & [StrapUI](http://strapui.com/)

##[Demo](http://rawgit.com/start-angular/ani-angular-2/master/dist/prod/index.html)

`Ani Angular2` provides the following features:

- Ready to go, statically typed build system using gulp for working with TypeScript.
- Production and development builds.
- Development server with Livereload.
- Following the best practices for your application’s structure.
- Manager of your type definitions using [typings](https://github.com/typings/typings).
- Basic Service Worker, which implements "Cache then network strategy".

## How to start

**Note** that this seed project requires node v4.x.x or higher and npm 2.14.7.


In order to start the seed use:
### Installation
####1. Clone this project or Download that ZIP file

```sh
$ git clone https://github.com/start-angular/SB-Admin-BS4-Angular-2.git
```

####2.  Make sure you have [npm](https://www.npmjs.org/) installed globally

You must have `ts-node` installed as global. If you don't, use:

```bash
npm install -g ts-node
```

####3. On the command prompt run the following commands

```sh
$ cd `project-directory`
```

```sh
$ npm install 
```

```sh
$ npm start
```

### Configuration

Default application server configuration

```javascript
var PORT             = 9000;
var LIVE_RELOAD_PORT = 9001;
var APP_BASE         = '/';
```

### Directory Structure

```
.
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── app
│   ├── layout
│   │   └── components
│   │       ├── app.css
│   │       ├── app.e2e.ts
│   │       ├── app.html
│   │       ├── app.ts
│   │       └── app.spec.ts
│   ├── assets
│   │   ├── images
│   │   │   └── flat-avatar.png
│   │   ├── bootstarp
│   │   ├── fontawesome-4.5.0
│   │   └── main.css
│   ├── pages
│   │   └── components
│   │       ├── blank-page
│   │       ├── components
│   │       └── login
│   ├── main.ts
│   └── index.html
├── dist
├── test
├── tools
│   ├── manual_typings
│   ├── tasks
│   ├── utils
│   ├── config.ts
│   └── utils.ts
├── appveyor.yml
├── gulpfile.ts
├── karma.conf.js
├── package.json
├── protractor.conf.js
├── test-main.js
├── tsconfig.json
├── tslint.json
└── typings.json
```
