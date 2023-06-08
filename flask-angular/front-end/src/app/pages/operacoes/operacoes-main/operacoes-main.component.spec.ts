import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OperacoesMainComponent } from './operacoes-main.component';

describe('OperacoesMainComponent', () => {
  let component: OperacoesMainComponent;
  let fixture: ComponentFixture<OperacoesMainComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OperacoesMainComponent]
    });
    fixture = TestBed.createComponent(OperacoesMainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
