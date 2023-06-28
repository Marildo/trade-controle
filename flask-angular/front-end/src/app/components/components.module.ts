import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TabComponent } from './tab/tab/tab.component';
import { TabHeaderComponent } from './tab/tab-header/tab-header.component';
import { TabBodyComponent } from './tab/tab-body/tab-body.component';
import { TabItemComponent } from './tab/tab-item/tab-item.component';
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
    ModalComponent
  ],


  exports: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent,
    ModalComponent,
  ],
})
export class ComponentsModule { }
