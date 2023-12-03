import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CarteiraHistoricoComponent } from './carteira-historico.component';

describe('CarteiraHistoricoComponent', () => {
  let component: CarteiraHistoricoComponent;
  let fixture: ComponentFixture<CarteiraHistoricoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CarteiraHistoricoComponent]
    });
    fixture = TestBed.createComponent(CarteiraHistoricoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
