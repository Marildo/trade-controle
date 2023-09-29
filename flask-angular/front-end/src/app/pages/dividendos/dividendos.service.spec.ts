import { TestBed } from '@angular/core/testing';

import { DividendosService } from './dividendos.service';

describe('DividendosService', () => {
  let service: DividendosService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DividendosService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
