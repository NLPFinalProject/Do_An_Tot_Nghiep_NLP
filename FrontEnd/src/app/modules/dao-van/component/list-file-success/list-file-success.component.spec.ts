import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ListFileSuccessComponent } from './list-file-success.component';

describe('ListFileSuccessComponent', () => {
  let component: ListFileSuccessComponent;
  let fixture: ComponentFixture<ListFileSuccessComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [ListFileSuccessComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(ListFileSuccessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
