import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardDaytradeComponent } from './dashboard-daytrade.component';

describe('DashboardDaytradeComponent', () => {
  let component: DashboardDaytradeComponent;
  let fixture: ComponentFixture<DashboardDaytradeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DashboardDaytradeComponent]
    });
    fixture = TestBed.createComponent(DashboardDaytradeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
