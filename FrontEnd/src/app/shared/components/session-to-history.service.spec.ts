import { TestBed } from '@angular/core/testing';

import { SessionToHistoryService } from './session-to-history.service';

describe('SessionToHistoryService', () => {
  let service: SessionToHistoryService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SessionToHistoryService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
