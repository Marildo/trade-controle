import { TestBed } from '@angular/core/testing';

import { AtivoService } from '../../service/api/ativo.service';

describe('AtivoService', () => {
  let service: AtivoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AtivoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});