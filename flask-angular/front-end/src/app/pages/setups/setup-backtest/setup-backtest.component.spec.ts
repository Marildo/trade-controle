import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetupBacktestComponent } from './setup-backtest.component';

describe('SetupBacktestComponent', () => {
  let component: SetupBacktestComponent;
  let fixture: ComponentFixture<SetupBacktestComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SetupBacktestComponent]
    });
    fixture = TestBed.createComponent(SetupBacktestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
