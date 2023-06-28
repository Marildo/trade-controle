import { Component, Input } from '@angular/core';

import { ParValues } from './par-value';

@Component({
  selector: 'app-panel-result',
  templateUrl: './panel-result.component.html',
  styleUrls: ['./panel-result.component.scss']
})
export class PanelResultComponent {
  @Input() values: ParValues[] = [];
}
