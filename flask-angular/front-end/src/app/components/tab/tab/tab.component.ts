import {
  Component, ContentChildren,
  QueryList,
  AfterContentInit,
  Input,
  AfterContentChecked,
} from '@angular/core';

import { Observable, Subscription } from "rxjs";
import { TabItemComponent } from '../tab-item/tab-item.component';
import { startWith, map, take, tap, delay } from "rxjs/operators";

@Component({
  selector: 'app-tab',
  templateUrl: './tab.component.html',
  styleUrls: ['./tab.component.scss']
})
export class TabComponent {


  @ContentChildren(TabItemComponent)
  tabs!: QueryList<TabItemComponent>;

  tabItems$!: Observable<TabItemComponent[]>;

  activeTab!: TabItemComponent;

  constructor() {

  }

  ngAfterContentInit(): void {
    this.tabItems$ = this.tabs.changes
      .pipe(startWith(""))
      .pipe(delay(0))
      .pipe(map(() => this.tabs.toArray()));
  }

  ngAfterContentChecked() {
    if (!this.activeTab) {
      Promise.resolve().then(() => {
        this.activeTab = this.tabs.first;
      });
    }
  }

  selectTab(tabItem: TabItemComponent) {
    if (this.activeTab === tabItem) {
      return;
    }

    if (this.activeTab) {
      this.activeTab.isActive = false;

    }

    this.activeTab = tabItem;

    tabItem.isActive = true;
  }

}
