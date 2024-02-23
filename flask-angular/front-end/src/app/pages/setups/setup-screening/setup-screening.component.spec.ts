import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetupScreeningComponent } from './setup-screening.component';

describe('SetupScreeningComponent', () => {
  let component: SetupScreeningComponent;
  let fixture: ComponentFixture<SetupScreeningComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SetupScreeningComponent]
    });
    fixture = TestBed.createComponent(SetupScreeningComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
