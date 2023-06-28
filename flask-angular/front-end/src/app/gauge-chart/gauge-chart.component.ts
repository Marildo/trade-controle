import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';

import { NgxGaugeType } from 'ngx-gauge/gauge/gauge';
 

@Component({
  selector: 'app-gauge-chart',
  templateUrl: './gauge-chart.component.html',
  styleUrls: ['./gauge-chart.component.scss']
})
export class GaugeChartComponent implements OnInit {


  // https://ashish-chopra.github.io/ngx-gauge/
  gaugeType:NgxGaugeType =  'full';
  gaugeValue = 90;
  gaugeLabel = "Speed";
  gaugeAppendText = "km/hr";


  ngOnInit(): void {
     
  }

 
    
}
