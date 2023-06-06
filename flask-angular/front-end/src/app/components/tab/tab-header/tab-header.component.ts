import { Component,TemplateRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-tab-header',
  templateUrl: './tab-header.component.html',
  styleUrls: ['./tab-header.component.scss']
})
export class TabHeaderComponent {

  @ViewChild(TemplateRef)
  labelContent!: TemplateRef<any>;

  constructor() {}

}
