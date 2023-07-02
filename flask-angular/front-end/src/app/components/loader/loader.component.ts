import { Component, OnInit } from '@angular/core';
import { LoaderService } from './loader.service';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
  styleUrls: ['./loader.component.scss']
})
export class LoaderComponent implements OnInit{

  public isShow = false

  constructor(private loader: LoaderService) {

  }

  ngOnInit(): void {
     this.loader.setComponent(this)
  }

  show():void {
    this.isShow = true
  }

  
  hide():void {
    this.isShow = false
  }


}
