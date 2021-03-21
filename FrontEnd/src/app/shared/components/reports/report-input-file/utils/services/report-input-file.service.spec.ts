import { TestBed } from '@angular/core/testing';

import { ReportInputFileService } from './report-input-file.service';

describe('ReportInputFileService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ReportInputFileService = TestBed.get(ReportInputFileService);
    expect(service).toBeTruthy();
  });
});
