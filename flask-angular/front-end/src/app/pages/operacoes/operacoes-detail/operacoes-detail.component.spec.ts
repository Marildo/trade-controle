import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacoesDetailComponent } from './operacoes-detail.component';

describe('OperacoesDetailComponent', () => {
  let component: OperacoesDetailComponent;
  let fixture: ComponentFixture<OperacoesDetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacoesDetailComponent]
    });
    fixture = TestBed.createComponent(OperacoesDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
