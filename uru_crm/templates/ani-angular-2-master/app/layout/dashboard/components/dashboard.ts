import {Component, ViewEncapsulation} from 'angular2/core';
import {
  RouteConfig,
  ROUTER_DIRECTIVES
} from 'angular2/router';

import {HomeCmp} from '../../../pages/home/components/home';
import {ComponentCmp} from '../../../pages/form-component/components/components';
import {BlankPageCmp} from '../../../pages/blank-page/components/blank_page';
import {SidebarCmp} from '../../../widgets/sidebar/components/sidebar';

@Component({
  selector: 'dashboard',
  templateUrl: './layout/dashboard/components/dashboard.html',
  encapsulation: ViewEncapsulation.None,
  directives: [ROUTER_DIRECTIVES, SidebarCmp]
})
@RouteConfig([
    { path: '/', component: HomeCmp, as: 'Home', useAsDefault:true},
    { path: '/camponents', component: ComponentCmp, as: 'Components' },
    { path: '/blank-page', component: BlankPageCmp, as: 'Blankpage' }
])
export class DashboardCmp { }
