import { Injectable } from '@angular/core';
import { ModalComponent } from './modal.component';

@Injectable({
  providedIn: 'root'
})
export class ModalService {


  private modals: ModalComponent[] = [];

  constructor() { }

  add(modal: ModalComponent) {
    if (!modal.id || this.modals.find(x => x.id === modal.id)) {
      throw new Error('Id do modal deve ser unico');
    }
    this.modals.push(modal);
  }


  remove(modal: ModalComponent) {
    this.modals = this.modals.filter(x => x === modal);
  }

  open(id: string) {
    const modal = this.find(id)
    modal.open();
  }

  close(id: string) {
    const modal = this.find(id)
    modal.close();
  }

  private find(id: string): ModalComponent {
    const modal = this.modals.find(x => x.id === id);
    if (!modal) {
      throw new Error(`modal '${id}' not found`);
    }
    return modal
  }
}