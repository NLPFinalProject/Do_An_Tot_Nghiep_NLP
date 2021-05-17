import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ValidateResultComponent } from './validate-result.component';

describe('ValidateResultComponent', () => {
  let component: ValidateResultComponent;
  let fixture: ComponentFixture<ValidateResultComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [ValidateResultComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(ValidateResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
