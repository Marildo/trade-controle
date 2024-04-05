import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtivosIbovespaItemComponent } from './ativos-ibovespa-item.component';

describe('AtivosIbovespaItemComponent', () => {
  let component: AtivosIbovespaItemComponent;
  let fixture: ComponentFixture<AtivosIbovespaItemComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AtivosIbovespaItemComponent]
    });
    fixture = TestBed.createComponent(AtivosIbovespaItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
