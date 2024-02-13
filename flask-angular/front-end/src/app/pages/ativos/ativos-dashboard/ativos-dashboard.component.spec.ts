import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtivosDashboardComponent } from './ativos-dashboard.component';

describe('AtivosDashboardComponent', () => {
  let component: AtivosDashboardComponent;
  let fixture: ComponentFixture<AtivosDashboardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AtivosDashboardComponent]
    });
    fixture = TestBed.createComponent(AtivosDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
