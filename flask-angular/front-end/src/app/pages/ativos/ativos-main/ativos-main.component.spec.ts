import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtivosMainComponent } from './ativos-main.component';

describe('AtivosMainComponent', () => {
  let component: AtivosMainComponent;
  let fixture: ComponentFixture<AtivosMainComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AtivosMainComponent]
    });
    fixture = TestBed.createComponent(AtivosMainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
