import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TabComponent } from './tab/tab/tab.component';
import { TabHeaderComponent } from './tab/tab-header/tab-header.component';
import { TabBodyComponent } from './tab/tab-body/tab-body.component';
import { TabItemComponent } from './tab/tab-item/tab-item.component';



@NgModule({
  declarations: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent
  ],
  imports: [
    CommonModule
  ],

  exports: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent
  ]
})
export class ComponentsModule { }
