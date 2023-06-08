import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacoesDashboardComponent } from './operacoes-dashboard.component';

describe('OperacoesDashboardComponent', () => {
  let component: OperacoesDashboardComponent;
  let fixture: ComponentFixture<OperacoesDashboardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacoesDashboardComponent]
    });
    fixture = TestBed.createComponent(OperacoesDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
