import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PanelResultComponent } from './panel-result.component';

describe('PanelResultComponent', () => {
  let component: PanelResultComponent;
  let fixture: ComponentFixture<PanelResultComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PanelResultComponent]
    });
    fixture = TestBed.createComponent(PanelResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
