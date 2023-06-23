import { Component } from '@angular/core';
import { ModalService } from 'src/app/components/modal/modal-service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  constructor(public modalService: ModalService){
    
  }

  openModal(){
    this.modalService.open('10')
  }

  closeModal(){
    this.modalService.close('10')
  }
}
