import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TabComponent } from './tab/tab/tab.component';
import { TabHeaderComponent } from './tab/tab-header/tab-header.component';
import { TabBodyComponent } from './tab/tab-body/tab-body.component';
import { TabItemComponent } from './tab/tab-item/tab-item.component';
import { PanelResultComponent } from './panel-result/panel-result.component';



@NgModule({
  declarations: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent,
    PanelResultComponent
  ],
  imports: [
    CommonModule
  ],

  exports: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent,
    PanelResultComponent
  ]
})
export class ComponentsModule { }
