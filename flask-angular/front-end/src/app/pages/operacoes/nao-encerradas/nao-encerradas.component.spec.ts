import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NaoEncerradasComponent } from './nao-encerradas.component';

describe('NaoEncerradasComponent', () => {
  let component: NaoEncerradasComponent;
  let fixture: ComponentFixture<NaoEncerradasComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NaoEncerradasComponent]
    });
    fixture = TestBed.createComponent(NaoEncerradasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
