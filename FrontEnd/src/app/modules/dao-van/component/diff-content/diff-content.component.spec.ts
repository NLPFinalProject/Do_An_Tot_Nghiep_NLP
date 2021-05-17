import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DiffContentComponent } from './diff-content.component';

describe('DiffContentComponent', () => {
  let component: DiffContentComponent;
  let fixture: ComponentFixture<DiffContentComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [DiffContentComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(DiffContentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
