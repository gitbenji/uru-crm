import {provide, enableProdMode} from 'angular2/core';
import {bootstrap} from 'angular2/platform/browser';
import {ROUTER_PROVIDERS, LocationStrategy, HashLocationStrategy} from 'angular2/router';
import {AppCmp} from './layout/base/components/app';

if ('<%= ENV %>' === 'prod') { enableProdMode(); }

bootstrap(AppCmp, [
	ROUTER_PROVIDERS,
	provide(LocationStrategy, { useClass: HashLocationStrategy })
]);
