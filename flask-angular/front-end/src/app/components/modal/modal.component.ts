import { Component, Input, OnInit } from '@angular/core';
import { ModalService } from './modal-service';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})

export class ModalComponent implements OnInit {

  @Input() id?: string;
  public isOpen = false;
 

  constructor(private modalService: ModalService) {
 
  }


  ngOnInit() {
    this.modalService.add(this);
  }

  ngOnDestroy() {
    this.modalService.remove(this);
  }


  open() {
    this.isOpen = true;
  }

  close() {
    this.isOpen = false;
  }

}
