import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CarteiraMovimentacoesComponent } from './carteira-movimentacoes.component';

describe('CarteiraMovimentacoesComponent', () => {
  let component: CarteiraMovimentacoesComponent;
  let fixture: ComponentFixture<CarteiraMovimentacoesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CarteiraMovimentacoesComponent]
    });
    fixture = TestBed.createComponent(CarteiraMovimentacoesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
