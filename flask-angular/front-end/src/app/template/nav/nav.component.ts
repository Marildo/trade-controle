import { Component } from '@angular/core';
import { LoaderService } from 'src/app/components/loader/loader.service';

@Component({
  selector: 'tc-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss']
})
export class NavComponent {

  constructor (private loader:LoaderService){}
}
