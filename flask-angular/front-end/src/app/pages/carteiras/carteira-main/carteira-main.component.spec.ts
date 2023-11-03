import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CarteiraMainComponent } from './carteira-main.component';

describe('CarteiraMainComponent', () => {
  let component: CarteiraMainComponent;
  let fixture: ComponentFixture<CarteiraMainComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CarteiraMainComponent]
    });
    fixture = TestBed.createComponent(CarteiraMainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
