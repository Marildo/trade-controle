import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtivosBacktestComponent } from './ativos-backtest.component';

describe('AtivosBacktestComponent', () => {
  let component: AtivosBacktestComponent;
  let fixture: ComponentFixture<AtivosBacktestComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AtivosBacktestComponent]
    });
    fixture = TestBed.createComponent(AtivosBacktestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
