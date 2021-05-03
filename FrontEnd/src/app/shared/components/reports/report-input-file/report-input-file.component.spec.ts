import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportInputFileComponent } from './report-input-file.component';

describe('ReportInputFileComponent', () => {
  let component: ReportInputFileComponent;
  let fixture: ComponentFixture<ReportInputFileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ReportInputFileComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportInputFileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
