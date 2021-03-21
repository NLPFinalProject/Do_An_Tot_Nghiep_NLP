import { TestBed } from '@angular/core/testing';

import { ListAccountService } from './list-account.service';

describe('ListAccountService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ListAccountService = TestBed.get(ListAccountService);
    expect(service).toBeTruthy();
  });
});
