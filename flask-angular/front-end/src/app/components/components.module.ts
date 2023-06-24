import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TabComponent } from './tab/tab/tab.component';
import { TabHeaderComponent } from './tab/tab-header/tab-header.component';
import { TabBodyComponent } from './tab/tab-body/tab-body.component';
import { TabItemComponent } from './tab/tab-item/tab-item.component';
import { PanelResultComponent } from './panel-result/panel-result.component';
import { ModalComponent } from './modal/modal.component';



@NgModule({
  imports: [
    CommonModule
  ],

  
  declarations: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent,
    PanelResultComponent,
    ModalComponent
  ],


  exports: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent,
    PanelResultComponent,
    ModalComponent,
  ],
})
export class ComponentsModule { }
