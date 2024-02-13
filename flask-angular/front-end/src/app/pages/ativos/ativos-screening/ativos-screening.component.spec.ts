import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtivosScreeningComponent } from './ativos-screening.component';

describe('AtivosScreeningComponent', () => {
  let component: AtivosScreeningComponent;
  let fixture: ComponentFixture<AtivosScreeningComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AtivosScreeningComponent]
    });
    fixture = TestBed.createComponent(AtivosScreeningComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
