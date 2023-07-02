import { Component } from '@angular/core';
import { LoaderService } from 'src/app/components/loader/loader.service';
import { ModalService } from 'src/app/components/modal/modal-service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  constructor(public modalService: ModalService,private loader: LoaderService){
    
  }

  openModal(){
    this.modalService.open('10')
  }

  closeModal(){
    this.modalService.close('10')
  }

  showLoader(){
    this.loader.show()
  }

  hideLoader(){
    this.loader.hide()
  }
}
