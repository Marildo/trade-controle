import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetupDashboardComponent } from './setup-dashboard.component';

describe('SetupDashboardComponent', () => {
  let component: SetupDashboardComponent;
  let fixture: ComponentFixture<SetupDashboardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SetupDashboardComponent]
    });
    fixture = TestBed.createComponent(SetupDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
