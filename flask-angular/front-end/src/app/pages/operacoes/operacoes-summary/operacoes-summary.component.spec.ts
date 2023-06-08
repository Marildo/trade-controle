import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacoesSummaryComponent } from './operacoes-summary.component';

describe('OperacoesSummaryComponent', () => {
  let component: OperacoesSummaryComponent;
  let fixture: ComponentFixture<OperacoesSummaryComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacoesSummaryComponent]
    });
    fixture = TestBed.createComponent(OperacoesSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
