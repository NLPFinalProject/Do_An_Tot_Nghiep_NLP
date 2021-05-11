import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ListFileDiffComponent } from './list-file-diff.component';

describe('ListFileDiffComponent', () => {
  let component: ListFileDiffComponent;
  let fixture: ComponentFixture<ListFileDiffComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [ListFileDiffComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(ListFileDiffComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
