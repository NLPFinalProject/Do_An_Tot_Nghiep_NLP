import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { IndexLoginComponent } from './index-login.component';

describe('IndexLoginComponent', () => {
  let component: IndexLoginComponent;
  let fixture: ComponentFixture<IndexLoginComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [IndexLoginComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(IndexLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
