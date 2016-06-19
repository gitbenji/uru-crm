import {Component} from 'angular2/core';
import {CAROUSEL_DIRECTIVES} from 'ng2-bootstrap/ng2-bootstrap';
@Component({
	selector: 'home',
	templateUrl: './pages/home/components/home.html',
	styleUrls: ['./pages/home/components/home.css'],
	directives: [CAROUSEL_DIRECTIVES]
})

export class HomeCmp {}
