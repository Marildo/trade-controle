import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TabComponent } from './tab/tab/tab.component';
import { TabHeaderComponent } from './tab/tab-header/tab-header.component';
import { TabBodyComponent } from './tab/tab-body/tab-body.component';
import { TabItemComponent } from './tab/tab-item/tab-item.component';
import { ModalComponent } from './modal/modal.component';
import { LoaderComponent } from './loader/loader.component';
import { LoaderService } from './loader/loader.service';



@NgModule({
  imports: [
    CommonModule
  ],

  
  declarations: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent,
    ModalComponent,
    LoaderComponent,
  ],

  providers: [
    LoaderService
  ],

  exports: [
    TabComponent,
    TabHeaderComponent,
    TabBodyComponent,
    TabItemComponent,
    ModalComponent,
    LoaderComponent,
  ],


})
export class ComponentsModule { }
