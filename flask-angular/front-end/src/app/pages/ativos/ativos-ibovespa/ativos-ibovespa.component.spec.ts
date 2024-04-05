import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtivosIbovespaComponent } from './ativos-ibovespa.component';

describe('AtivosIbovespaComponent', () => {
  let component: AtivosIbovespaComponent;
  let fixture: ComponentFixture<AtivosIbovespaComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AtivosIbovespaComponent]
    });
    fixture = TestBed.createComponent(AtivosIbovespaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
