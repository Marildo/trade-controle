import { Component, Input, ContentChild } from '@angular/core';
import { TabHeaderComponent } from '../tab-header/tab-header.component';
import { TabBodyComponent } from '../tab-body/tab-body.component';


@Component({
  selector: 'app-tab-item',
  templateUrl: './tab-item.component.html',
  styleUrls: ['./tab-item.component.scss']
})
export class TabItemComponent {

  @Input()
  label!: string;

  @Input()
  isActive!: boolean;


  @ContentChild(TabBodyComponent)
  bodyComponent!: TabBodyComponent;

  @ContentChild(TabHeaderComponent)
  headerComponent!: TabHeaderComponent;

  constructor() { }

  ngOnInit(): void { }

}
