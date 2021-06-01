import { TestBed } from '@angular/core/testing';

import { DaovanServiceService } from './daovan-service.service';

describe('DaovanServiceService', () => {
  let service: DaovanServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DaovanServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
