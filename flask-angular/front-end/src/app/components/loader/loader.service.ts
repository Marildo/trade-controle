import { Injectable } from '@angular/core';
import { LoaderComponent } from './loader.component';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {

  private component!: LoaderComponent;

  constructor() { }

  public setComponent(component: LoaderComponent):void {
    this.component  = component
  }

  public show():void{
    this.component.show()
  }

  public hide():void{
    this.component.hide()
  }
}
