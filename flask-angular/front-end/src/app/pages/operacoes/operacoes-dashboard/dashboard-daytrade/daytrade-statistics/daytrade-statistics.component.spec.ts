import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DaytradeStatisticsComponent } from './daytrade-statistics.component';

describe('DaytradeStatisticsComponent', () => {
  let component: DaytradeStatisticsComponent;
  let fixture: ComponentFixture<DaytradeStatisticsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DaytradeStatisticsComponent]
    });
    fixture = TestBed.createComponent(DaytradeStatisticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
