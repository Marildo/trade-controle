import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DividendosComponent } from './dividendos.component';

describe('DividendosComponent', () => {
  let component: DividendosComponent;
  let fixture: ComponentFixture<DividendosComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DividendosComponent]
    });
    fixture = TestBed.createComponent(DividendosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
