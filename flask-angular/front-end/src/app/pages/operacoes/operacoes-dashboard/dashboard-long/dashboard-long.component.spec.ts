import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardLongComponent } from './dashboard-long.component';

describe('DashboardLongComponent', () => {
  let component: DashboardLongComponent;
  let fixture: ComponentFixture<DashboardLongComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DashboardLongComponent]
    });
    fixture = TestBed.createComponent(DashboardLongComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
