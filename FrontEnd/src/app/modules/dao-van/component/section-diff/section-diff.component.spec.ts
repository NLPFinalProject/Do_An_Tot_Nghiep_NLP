import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SectionDiffComponent } from './section-diff.component';

describe('SectionDiffComponent', () => {
  let component: SectionDiffComponent;
  let fixture: ComponentFixture<SectionDiffComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [SectionDiffComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(SectionDiffComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
