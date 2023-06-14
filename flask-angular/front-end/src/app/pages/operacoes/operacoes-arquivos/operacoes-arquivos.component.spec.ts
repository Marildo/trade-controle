import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacoesArquivosComponent } from './operacoes-arquivos.component';

describe('OperacoesArquivosComponent', () => {
  let component: OperacoesArquivosComponent;
  let fixture: ComponentFixture<OperacoesArquivosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacoesArquivosComponent]
    });
    fixture = TestBed.createComponent(OperacoesArquivosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
