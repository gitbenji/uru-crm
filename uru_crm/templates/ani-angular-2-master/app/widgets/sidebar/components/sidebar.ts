import {Component} from 'angular2/core';
import {
	RouteConfig,
	Router,
	ROUTER_DIRECTIVES
} from 'angular2/router';

import {HomeCmp} from '../../../pages/home/components/home';
import {ComponentCmp} from '../../../pages/form-component/components/components';
import {BlankPageCmp} from '../../../pages/blank-page/components/blank_page';
@Component({
	selector: 'sidebar',
	templateUrl: './widgets/sidebar/components/sidebar.html',
	directives: [ROUTER_DIRECTIVES]
})
@RouteConfig([
	{ path: '/', component: HomeCmp, as: 'Home', useAsDefault: true },
	{ path: '/components', component: ComponentCmp, as: 'Components' },
	{ path: '/blank-page', component: BlankPageCmp, as: 'Blankpage' },
])

export class SidebarCmp {
	showMenu: string = '';
	constructor(private _router: Router) {}
	addExpandClass(element) {
		if (element === this.showMenu) {
			this.showMenu = '0';
		} else {
			this.showMenu = element;
		}
	}
	gotoLogin() {
		this._router.navigate(['Login']);
	}
}
