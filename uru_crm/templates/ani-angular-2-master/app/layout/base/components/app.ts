import {Component, ViewEncapsulation} from 'angular2/core';
import {
    RouteConfig,
    ROUTER_DIRECTIVES
} from 'angular2/router';

import {LoginCmp} from '../../../pages/login/components/login';
import {DashboardCmp} from '../../dashboard/components/dashboard';

@Component({
  selector: 'app',
  templateUrl: './layout/base/components/app.html',
  styleUrls: ['./layout/base/components/app.css'],
  encapsulation: ViewEncapsulation.None,
  directives: [ROUTER_DIRECTIVES]
})
@RouteConfig([
  { path: '/login', component: LoginCmp, as: 'Login', useAsDefault:true},
  { path: '/dashboard/...', component: DashboardCmp, as: 'Dashboard' }
])
export class AppCmp { }
